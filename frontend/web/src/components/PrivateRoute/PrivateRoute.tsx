import { Navigate } from 'react-router-dom';
import React, { ReactNode } from 'react';
import useUserStore from '@/stores/UserStore';

export default function PrivateRoute({ children }: { children: ReactNode }): React.JSX.Element {
  const userStore = useUserStore();
  return userStore.loggedIn ? <>{children}</> : <Navigate to="/" />;
}
