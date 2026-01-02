/**
 * Authentication API Service
 */

import apiClient from './client';

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
  phone?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  avatar_url?: string;
  phone?: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Register a new user
 */
export async function register(data: RegisterData): Promise<User> {
  return apiClient.post<User>('/api/v1/auth/register', data);
}

/**
 * Login user
 */
export async function login(data: LoginData): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', data);
  
  // Store tokens
  apiClient.setToken(response.access_token);
  localStorage.setItem('refresh_token', response.refresh_token);
  
  return response;
}

/**
 * Logout user
 */
export function logout(): void {
  apiClient.removeToken();
}

/**
 * Get current user info
 */
export async function getCurrentUser(): Promise<User> {
  return apiClient.get<User>('/api/v1/auth/me', true);
}

/**
 * Refresh access token
 */
export async function refreshToken(): Promise<TokenResponse> {
  const refreshToken = localStorage.getItem('refresh_token');
  
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await apiClient.post<TokenResponse>('/api/v1/auth/refresh', {
    refresh_token: refreshToken,
  });

  // Update tokens
  apiClient.setToken(response.access_token);
  localStorage.setItem('refresh_token', response.refresh_token);

  return response;
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return localStorage.getItem('access_token') !== null;
}
