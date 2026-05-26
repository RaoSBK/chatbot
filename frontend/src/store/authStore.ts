// Simple state management store placeholder for authStore
import { create } from 'zustand';

interface StoreState {
  items: any[];
  addItem: (item: any) => void;
  clear: () => void;
}

export const useauthStore = create<StoreState>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  clear: () => set({ items: [] })
}));
