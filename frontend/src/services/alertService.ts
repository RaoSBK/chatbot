import { api } from '../lib/api';

export const alertService = {
  async getAll() {
    return api.get('/alert');
  },
  
  async getById(id: string) {
    return api.get(`/alert/${id}`);
  },
  
  async create(data: any) {
    return api.post('/alert', data);
  }
};
