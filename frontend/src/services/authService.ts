import { api } from '../lib/api';

export const authService = {
  async getAll() {
    return api.get('/auth');
  },
  
  async getById(id: string) {
    return api.get(`/auth/${id}`);
  },
  
  async create(data: any) {
    return api.post('/auth', data);
  }
};
