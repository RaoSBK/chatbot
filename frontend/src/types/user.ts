export interface User {
  id: string;
  full_name: string | null;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AccessTokenResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterPayload {
  full_name?: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}
