import { api } from '../lib/api';

export const chatService = {
  async getAll() {
    return api.get('/chat');
  },
  
  async getById(id: string) {
    return api.get(`/chat/${id}`);
  },
  
  async create(data: any) {
    return api.post('/chat', data);
  }
};
