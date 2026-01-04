"""
Comprehensive test script for appointment system enhancements
Tests: Time conflict checking, technician scheduling, store admin management
"""
import requests
import json
from datetime import date, time

BASE_URL = "http://localhost:8000/api/v1"

def login(phone, password):
    """Login and get access token"""
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"phone": phone, "password": password}
    )
    return resp.json()["access_token"]

def test_time_conflict_checking():
    """Test time conflict detection for technicians and users"""
    print("\n" + "="*60)
    print("TEST 1: Time Conflict Checking")
    print("="*60)
    
    token = login("13800138000", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1.1: Try to create appointment that conflicts with technician
    print("\n1.1 Testing technician time conflict...")
    resp = requests.post(
        f"{BASE_URL}/appointments/",
        headers=headers,
        json={
            "store_id": 4,
            "service_id": 30001,
            "technician_id": 1,
            "appointment_date": "2026-01-10",
            "appointment_time": "10:15:00"  # Conflicts with 10:00-10:30
        }
    )
    if resp.status_code == 400 and "technician" in resp.json()["detail"].lower():
        print("   ✅ Technician conflict detected correctly")
    else:
        print(f"   ❌ Expected conflict error, got: {resp.status_code} - {resp.json()}")
    
    # Test 1.2: Create a valid appointment
    print("\n1.2 Creating valid appointment...")
    resp = requests.post(
        f"{BASE_URL}/appointments/",
        headers=headers,
        json={
            "store_id": 4,
            "service_id": 30001,
            "technician_id": 1,
            "appointment_date": "2026-01-11",
            "appointment_time": "11:00:00"
        }
    )
    if resp.status_code == 201:
        appt_id = resp.json()["id"]
        print(f"   ✅ Appointment created successfully (ID: {appt_id})")
        return appt_id
    else:
        print(f"   ❌ Failed to create appointment: {resp.json()}")
        return None

def test_technician_scheduling(appt_id):
    """Test technician appointment list and available slots"""
    print("\n" + "="*60)
    print("TEST 2: Technician Scheduling")
    print("="*60)
    
    # Test 2.1: Get technician appointments
    print("\n2.1 Getting technician appointments...")
    resp = requests.get(f"{BASE_URL}/technicians/1/appointments?date=2026-01-10")
    if resp.status_code == 200:
        appointments = resp.json()
        print(f"   ✅ Found {len(appointments)} appointments on 2026-01-10")
        for appt in appointments:
            print(f"      - {appt['appointment_time']}: {appt['service_name']} ({appt['status']})")
    else:
        print(f"   ❌ Failed: {resp.json()}")
    
    # Test 2.2: Get available slots
    print("\n2.2 Getting available time slots...")
    resp = requests.get(
        f"{BASE_URL}/technicians/1/available-slots",
        params={"date": "2026-01-10", "service_id": 30001}
    )
    if resp.status_code == 200:
        slots = resp.json()
        print(f"   ✅ Found {len(slots)} available slots")
        print(f"      First 3 slots: {[s['start_time'] for s in slots[:3]]}")
    else:
        print(f"   ❌ Failed: {resp.json()}")

def test_store_admin_management():
    """Test store admin appointment management"""
    print("\n" + "="*60)
    print("TEST 3: Store Admin Management")
    print("="*60)
    
    token = login("13800138000", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 3.1: Get store appointments
    print("\n3.1 Getting store appointments...")
    resp = requests.get(f"{BASE_URL}/stores/4/appointments", headers=headers)
    if resp.status_code == 200:
        appointments = resp.json()
        print(f"   ✅ Found {len(appointments)} appointments for store 4")
    else:
        print(f"   ❌ Failed: {resp.json()}")
    
    # Test 3.2: Get appointment statistics
    print("\n3.2 Getting appointment statistics...")
    resp = requests.get(f"{BASE_URL}/stores/4/appointments/stats", headers=headers)
    if resp.status_code == 200:
        stats = resp.json()
        print(f"   ✅ Statistics retrieved:")
        print(f"      Today: {stats['today']['total']} total")
        print(f"      This week: {stats['this_week']['total']} total ({stats['this_week']['pending']} pending)")
        print(f"      This month: {stats['this_month']['total']} total")
    else:
        print(f"   ❌ Failed: {resp.json()}")
    
    # Test 3.3: Confirm an appointment
    print("\n3.3 Testing appointment confirmation...")
    # First create a pending appointment
    resp = requests.post(
        f"{BASE_URL}/appointments/",
        headers=headers,
        json={
            "store_id": 4,
            "service_id": 30003,
            "technician_id": 1,
            "appointment_date": "2026-01-12",
            "appointment_time": "15:00:00"
        }
    )
    if resp.status_code == 201:
        new_appt_id = resp.json()["id"]
        print(f"      Created pending appointment (ID: {new_appt_id})")
        
        # Confirm it
        resp = requests.patch(
            f"{BASE_URL}/appointments/{new_appt_id}/confirm",
            headers=headers
        )
        if resp.status_code == 200 and resp.json()["status"] == "confirmed":
            print(f"   ✅ Appointment confirmed successfully")
        else:
            print(f"   ❌ Failed to confirm: {resp.json()}")
    else:
        print(f"   ❌ Failed to create test appointment: {resp.json()}")

def test_status_flow_rules():
    """Test appointment status transition rules"""
    print("\n" + "="*60)
    print("TEST 4: Status Flow Rules")
    print("="*60)
    
    token = login("13800138000", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 4.1: Try to confirm a cancelled appointment (should fail)
    print("\n4.1 Testing invalid status transition...")
    # Create and cancel an appointment
    resp = requests.post(
        f"{BASE_URL}/appointments/",
        headers=headers,
        json={
            "store_id": 4,
            "service_id": 30001,
            "technician_id": 1,
            "appointment_date": "2026-01-13",
            "appointment_time": "10:00:00"
        }
    )
    if resp.status_code == 201:
        appt_id = resp.json()["id"]
        
        # Cancel it
        requests.delete(f"{BASE_URL}/appointments/{appt_id}", headers=headers)
        
        # Try to confirm cancelled appointment
        resp = requests.patch(
            f"{BASE_URL}/appointments/{appt_id}/confirm",
            headers=headers
        )
        if resp.status_code == 400:
            print(f"   ✅ Invalid transition blocked: {resp.json()['detail']}")
        else:
            print(f"   ❌ Should have blocked invalid transition")
    
    # Test 4.2: Valid status flow
    print("\n4.2 Testing valid status flow (pending -> confirmed -> completed)...")
    resp = requests.post(
        f"{BASE_URL}/appointments/",
        headers=headers,
        json={
            "store_id": 4,
            "service_id": 30002,
            "technician_id": 1,
            "appointment_date": "2026-01-14",
            "appointment_time": "14:00:00"
        }
    )
    if resp.status_code == 201:
        appt_id = resp.json()["id"]
        print(f"      Created pending appointment (ID: {appt_id})")
        
        # Confirm
        resp = requests.patch(f"{BASE_URL}/appointments/{appt_id}/confirm", headers=headers)
        if resp.status_code == 200:
            print(f"      ✓ Confirmed")
            
            # Complete
            resp = requests.patch(f"{BASE_URL}/appointments/{appt_id}/complete", headers=headers)
            if resp.status_code == 200 and resp.json()["status"] == "completed":
                print(f"   ✅ Valid status flow completed successfully")
            else:
                print(f"   ❌ Failed to complete: {resp.json()}")
        else:
            print(f"   ❌ Failed to confirm: {resp.json()}")

def main():
    print("\n" + "="*60)
    print("APPOINTMENT SYSTEM ENHANCEMENTS - COMPREHENSIVE TEST")
    print("="*60)
    
    try:
        appt_id = test_time_conflict_checking()
        test_technician_scheduling(appt_id)
        test_store_admin_management()
        test_status_flow_rules()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
