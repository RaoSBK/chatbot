'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '../store/authStore';

/**
 * useAuth — convenience hook.
 *
 * @param requireAuth   If true, redirects to /login when user is not authenticated
 *                      after initialization is complete.
 * @param redirectIfAuth If true, redirects to / when user IS already authenticated
 *                      (useful for login / register pages).
 */
export function useAuth(
  options: { requireAuth?: boolean; redirectIfAuth?: boolean } = {},
) {
  const { requireAuth = false, redirectIfAuth = false } = options;
  const router = useRouter();
  const {
    user,
    accessToken,
    isAuthenticated,
    isLoading,
    initialize,
    logout,
  } = useAuthStore();

  useEffect(() => {
    initialize();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (isLoading) return;

    if (requireAuth && !isAuthenticated) {
      router.replace('/login');
    }
    if (redirectIfAuth && isAuthenticated) {
      router.replace('/');
    }
  }, [isLoading, isAuthenticated, requireAuth, redirectIfAuth, router]);

  return { user, accessToken, isAuthenticated, isLoading, logout };
}
