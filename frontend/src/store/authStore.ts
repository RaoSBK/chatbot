'use client';

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { authService } from '../services/authService';
import type { User } from '../types/user';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setTokenAndUser: (token: string, user: User) => void;
  logout: () => Promise<void>;
  refreshAccessToken: () => Promise<boolean>;
  fetchCurrentUser: () => Promise<void>;
  initialize: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,
      isLoading: true,

      setTokenAndUser: (token, user) =>
        set({ accessToken: token, user, isAuthenticated: true, isLoading: false }),

      logout: async () => {
        try { await authService.logout(); } catch { /* ignore */ }
        set({ user: null, accessToken: null, isAuthenticated: false, isLoading: false });
      },

      refreshAccessToken: async () => {
        try {
          const data = await authService.refresh();
          set({ accessToken: data.access_token });
          return true;
        } catch {
          set({ user: null, accessToken: null, isAuthenticated: false });
          return false;
        }
      },

      fetchCurrentUser: async () => {
        const token = get().accessToken;
        if (!token) return;
        try {
          const user = await authService.getMe(token);
          set({ user, isAuthenticated: true });
        } catch {
          // access token expired — try refresh
          const ok = await get().refreshAccessToken();
          if (ok) {
            const newToken = get().accessToken!;
            try {
              const user = await authService.getMe(newToken);
              set({ user, isAuthenticated: true });
            } catch {
              set({ user: null, accessToken: null, isAuthenticated: false });
            }
          }
        }
      },

      initialize: async () => {
        set({ isLoading: true });
        const { accessToken } = get();
        if (accessToken) {
          await get().fetchCurrentUser();
        } else {
          // Try silent refresh using HttpOnly cookie
          const ok = await get().refreshAccessToken();
          if (ok) await get().fetchCurrentUser();
        }
        set({ isLoading: false });
      },
    }),
    {
      name: 'mmx-auth',
      storage: createJSONStorage(() => sessionStorage), // sessionStorage: cleared on tab close
      partialize: (state) => ({
        accessToken: state.accessToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    },
  ),
);
