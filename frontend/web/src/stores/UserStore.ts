import { create } from 'zustand';

export type UserState = {
  loggedIn: boolean;
};
const useUserStore = create<UserState>(() => ({
  loggedIn: true,
}));

export default useUserStore;
