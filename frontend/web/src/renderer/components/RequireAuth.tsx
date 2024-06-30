import { Navigate, Outlet } from "react-router-dom";
import { useContext } from "use-context-selector";
import { UserContext } from "../contexts/UserContext";

export default () => {
    const { getIsLoggedIn } = useContext(UserContext);

    if (!getIsLoggedIn()) {
        // Redirect to login page
        return (
            <Navigate
                replace
                to="/login"
            />
        );
    }

    // If user is logged in, render the child components
    return <Outlet />;
};
