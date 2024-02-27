import { createRoot } from "react-dom/client";
import { App } from "./pages/App";
import { createBrowserRouter, createHashRouter, RouterProvider } from "react-router-dom";
import { Portal } from "./pages/Portal";

const router = createHashRouter([
    {
        path: "/",
        element: <Portal />,
    },
    {
        path: "/workflows/:id",
        element: <App />,
    },
]);

const container = document.getElementById("root");
const root = createRoot(container!);
root.render(<App />);
