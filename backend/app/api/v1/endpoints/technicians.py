"""
Technicians API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db, get_current_admin_user, get_current_store_admin
from app.models.user import User
from app.crud import technician as crud_technician
from app.schemas.technician import Technician, TechnicianCreate, TechnicianUpdate

router = APIRouter()


@router.get("/", response_model=List[Technician])
def get_technicians(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    store_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of technicians with optional filters
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **store_id**: Filter by store ID
    """
    technicians = crud_technician.get_technicians(
        db,
        skip=skip,
        limit=limit,
        store_id=store_id
    )
    return technicians


@router.get("/{technician_id}", response_model=Technician)
def get_technician(
    technician_id: int,
    db: Session = Depends(get_db)
):
    """
    Get technician details by ID
    """
    technician = crud_technician.get_technician(db, technician_id=technician_id)
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")
    
    return technician


@router.post("/", response_model=Technician, status_code=201)
def create_technician(
    technician: TechnicianCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_store_admin)
):
    """
    Create a new technician (Store admin only)
    
    - Super admin can create technicians for any store
    - Store manager can only create technicians for their own store
    """
    # If user is store manager (not super admin), enforce store ownership
    if not current_user.is_admin:
        if technician.store_id != current_user.store_id:
            raise HTTPException(
                status_code=403,
                detail="You can only create technicians for your own store"
            )
    
    new_technician = crud_technician.create_technician(db, technician=technician)
    return new_technician


@router.patch("/{technician_id}", response_model=Technician)
def update_technician(
    technician_id: int,
    technician: TechnicianUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_store_admin)
):
    """
    Update technician information (Store admin only)
    
    - Super admin can update technicians from any store
    - Store manager can only update technicians from their own store
    """
    # Get existing technician
    existing_technician = crud_technician.get_technician(db, technician_id=technician_id)
    if not existing_technician:
        raise HTTPException(status_code=404, detail="Technician not found")
    
    # If user is store manager (not super admin), enforce store ownership
    if not current_user.is_admin:
        if existing_technician.store_id != current_user.store_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update technicians from your own store"
            )
    
    updated_technician = crud_technician.update_technician(
        db,
        technician_id=technician_id,
        technician=technician
    )
    return updated_technician


@router.delete("/{technician_id}", status_code=204)
def delete_technician(
    technician_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_store_admin)
):
    """
    Delete a technician (Store admin only)
    
    - Super admin can delete technicians from any store
    - Store manager can only delete technicians from their own store
    """
    technician = crud_technician.get_technician(db, technician_id=technician_id)
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")
    
    # If user is store manager (not super admin), enforce store ownership
    if not current_user.is_admin:
        if technician.store_id != current_user.store_id:
            raise HTTPException(
                status_code=403,
                detail="You can only delete technicians from your own store"
            )
    
    crud_technician.delete_technician(db, technician_id=technician_id)
    return None


@router.patch("/{technician_id}/availability", response_model=Technician)
def toggle_technician_availability(
    technician_id: int,
    is_active: int = Query(..., ge=0, le=1, description="0 for inactive, 1 for active"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_store_admin)
):
    """
    Toggle technician availability (Store admin only)
    
    - Super admin can toggle availability for technicians from any store
    - Store manager can only toggle availability for technicians from their own store
    """
    technician = crud_technician.get_technician(db, technician_id=technician_id)
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")
    
    # If user is store manager (not super admin), enforce store ownership
    if not current_user.is_admin:
        if technician.store_id != current_user.store_id:
            raise HTTPException(
                status_code=403,
                detail="You can only toggle availability for technicians from your own store"
            )
    
    updated_technician = crud_technician.update_technician(
        db,
        technician_id=technician_id,
        technician=TechnicianUpdate(is_active=is_active)
    )
    return updated_technician
