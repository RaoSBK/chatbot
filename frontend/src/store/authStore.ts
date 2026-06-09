import { create } from 'zustand';
import { authService } from '../services/authService';

export interface User {
  id: string;
  email: string;
  full_name?: string | null;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (credentials: { email: string; password: string }) => Promise<{ success: boolean; error?: string }>;
  register: (data: { full_name?: string; email: string; password: string }) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  initialize: () => void;
}

const decodeJwt = (token: string) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      window
        .atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
};

export const useauthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (credentials) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.login(credentials);
      if (response && response.access_token) {
        const token = response.access_token;
        localStorage.setItem('token', token);
        const payload = decodeJwt(token);
        const user: User = {
          id: payload?.sub || '',
          email: credentials.email,
        };
        localStorage.setItem('user', JSON.stringify(user));
        set({
          token,
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null
        });
        return { success: true };
      } else {
        const errorMsg = response?.detail || 'Invalid login response';
        set({ error: errorMsg, isLoading: false });
        return { success: false, error: errorMsg };
      }
    } catch (err: any) {
      const errorMsg = err?.message || 'Login failed';
      set({ error: errorMsg, isLoading: false });
      return { success: false, error: errorMsg };
    }
  },

  register: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.register(data);
      // If the backend returns the registered user info, we can log them in next
      if (response && response.email) {
        set({ isLoading: false, error: null });
        return { success: true };
      } else {
        const errorMsg = response?.detail || 'Registration failed';
        set({ error: errorMsg, isLoading: false });
        return { success: false, error: errorMsg };
      }
    } catch (err: any) {
      const errorMsg = err?.message || 'Registration failed';
      set({ error: errorMsg, isLoading: false });
      return { success: false, error: errorMsg };
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null
    });
  },

  initialize: () => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      const userStr = localStorage.getItem('user');
      if (token) {
        set({
          token,
          user: userStr ? JSON.parse(userStr) : null,
          isAuthenticated: true,
        });
      }
    }
  }
}));
