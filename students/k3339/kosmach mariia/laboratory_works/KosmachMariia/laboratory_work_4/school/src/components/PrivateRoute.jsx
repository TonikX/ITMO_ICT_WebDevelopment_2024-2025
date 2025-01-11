import { Navigate, Outlet } from "react-router-dom";
import useUser from "../hooks/useUser";
import Login from "../page/Login";

export const PrivateRoute = () => {
  const { token } = useUser();

  return token ? (
    <Outlet />
  ) : (
    <Navigate to="/login" element={<Login />} replase />
  );
};