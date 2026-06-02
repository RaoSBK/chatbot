import type {
  AccessTokenResponse,
  LoginPayload,
  RegisterPayload,
  TokenResponse,
  User,
} from '../types/user';

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

// ─── error helpers ───────────────────────────────────────────────────────────

function friendlyError(err: unknown): string {
  if (err instanceof Error) {
    if (err.message.toLowerCase().includes('failed to fetch') ||
        err.message.toLowerCase().includes('networkerror') ||
        err.message.toLowerCase().includes('connection refused')) {
      return 'Cannot connect to the server. Make sure the backend is running on port 8000.';
    }
    return err.message;
  }
  return 'An unexpected error occurred.';
}


async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  token?: string,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  try {
    const res = await fetch(`${BASE}${path}`, {
      ...options,
      headers,
      credentials: 'include', // send/receive HttpOnly cookies
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body?.detail ?? `HTTP ${res.status}`);
    }
    return res.json() as Promise<T>;
  } catch (err) {
    throw new Error(friendlyError(err));
  }
}

// ─── public API ──────────────────────────────────────────────────────────────

export const authService = {
  /** Register a new account. Returns the created user profile. */
  register: (payload: RegisterPayload): Promise<User> =>
    apiFetch<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  /**
   * Login with email + password (sent as OAuth2 form data).
   * Backend sets an HttpOnly refresh-token cookie automatically.
   */
  login: async (payload: LoginPayload): Promise<TokenResponse> => {
    const form = new URLSearchParams();
    form.append('username', payload.email);
    form.append('password', payload.password);

    try {
      const res = await fetch(`${BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        credentials: 'include',
        body: form.toString(),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.detail ?? `HTTP ${res.status}`);
      }
      return res.json() as Promise<TokenResponse>;
    } catch (err) {
      throw new Error(friendlyError(err));
    }
  },

  /**
   * Exchange the HttpOnly refresh-token cookie for a new access token.
   * The backend also rotates the cookie (forward secrecy).
   */
  refresh: (): Promise<AccessTokenResponse> =>
    apiFetch<AccessTokenResponse>('/auth/refresh', { method: 'POST' }),

  /** Clear the refresh-token cookie server-side. */
  logout: (): Promise<{ message: string }> =>
    apiFetch('/auth/logout', { method: 'POST' }),

  /** Fetch the current user's profile (requires Bearer token). */
  getMe: (token: string): Promise<User> =>
    apiFetch<User>('/auth/me', {}, token),
};
