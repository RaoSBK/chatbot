import { api } from '../lib/api';

export const goalService = {
  async getAll() {
    return api.get('/goal');
  },
  
  async getById(id: string) {
    return api.get(`/goal/${id}`);
  },
  
  async create(data: any) {
    return api.post('/goal', data);
  }
};
