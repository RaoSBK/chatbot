import { api } from '../lib/api';

export const stressService = {
  async getAll() {
    return api.get('/stress');
  },
  
  async getById(id: string) {
    return api.get(`/stress/${id}`);
  },
  
  async create(data: any) {
    return api.post('/stress', data);
  }
};
