import { api } from '../lib/api';

export const personalityService = {
  async getAll() {
    return api.get('/personality');
  },
  
  async getById(id: string) {
    return api.get(`/personality/${id}`);
  },
  
  async create(data: any) {
    return api.post('/personality', data);
  }
};
