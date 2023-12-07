import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './pages/Home.page';
import WorkflowEditorPage from './pages/WorkflowsEditor.page';

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/workflows',
    element: <WorkflowEditorPage />,
  },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
