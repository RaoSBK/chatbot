import { api } from '../lib/api';

export const authService = {
  async register(data: any) {
    return api.post('/auth/register', data);
  },

  async login(credentials: { email: string; password: string }) {
    return api.post('/auth/login', credentials);
  },
  async create(data: any) {
    return this.register(data);
  }
};
