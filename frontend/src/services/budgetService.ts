import { api } from '../lib/api';

export const budgetService = {
  async getAll() {
    return api.get('/budget');
  },
  
  async getById(id: string) {
    return api.get(`/budget/${id}`);
  },
  
  async create(data: any) {
    return api.post('/budget', data);
  }
};
