import { api } from '../lib/api';

export const expenseService = {
  async getAll() {
    return api.get('/expense');
  },
  
  async getById(id: string) {
    return api.get(`/expense/${id}`);
  },
  
  async create(data: any) {
    return api.post('/expense', data);
  }
};
