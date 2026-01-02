/**
 * Protected Route Component
 * Redirects to login if user is not authenticated
 */

import { Navigate } from 'react-router-dom';
import { apiClient } from '../api/client';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  // Check if user has access token
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    // Redirect to login if not authenticated
    return <Navigate to="/login" replace />;
  }
  
  // Render children if authenticated
  return <>{children}</>;
}
