import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './pages/Home.page';
import WorkflowEditorPage from './pages/WorkflowsEditor.page';
import PortalPage from './pages/Portal.page';
import useFlowStore from './stores/FlowStore';

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/workflows',
    element: <PortalPage />,
  },
  {
    path: '/workflows/:id',
    element: <WorkflowEditorPage />,
    action: async (args) => {
      useFlowStore.getState().loadWorkflow(args.params.id!);
    },
  },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
