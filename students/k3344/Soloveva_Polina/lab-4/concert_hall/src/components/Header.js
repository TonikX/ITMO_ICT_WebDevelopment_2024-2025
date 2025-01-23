import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../utils/AuthContext";

const Header = () => {
  const { userRole, isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-dark bg-dark p-3">
      <div className="container d-flex justify-content-between">
        <Link className="navbar-brand" to="/">Concert Hall</Link>

        {isAuthenticated ? (
          <div>
            {userRole === "user" ? (
              <Link className="btn btn-outline-light me-2" to="/orders/my">Мои заказы</Link>
            ) : (
              <Link className="btn btn-outline-light me-2" to="/admin">Админ-панель</Link>
            )}
            <button className="btn btn-danger" onClick={handleLogout}>Выйти</button>
          </div>
        ) : (
          <Link className="btn btn-outline-light" to="/login">Войти</Link>
        )}
      </div>
    </nav>
  );
};

export default Header;
