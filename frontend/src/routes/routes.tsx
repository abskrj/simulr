import { createBrowserRouter } from "react-router";
import Dashboard from "../pages/dashboard";
import ProjectPage from "../pages/project/ProjectPage";

const routes = createBrowserRouter([
    {
        path: "/",
        element: <Dashboard />,
    },
    {
        path: "/project/:projectId",
        element: <ProjectPage />
    },
    {
        path: "/project/new",
        element: <ProjectPage />
    }
]);

export default routes;