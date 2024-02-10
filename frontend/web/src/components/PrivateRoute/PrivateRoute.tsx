import { Navigate } from 'react-router-dom';
import React, { ReactNode } from 'react';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export default function PrivateRoute({ children }: { children: ReactNode }): React.JSX.Element {
  // const userStore = useUserStore();
  // return userStore.loggedIn ? <>{children}</> : <Navigate to="/" />;
  return <Navigate to="/" />;
}
