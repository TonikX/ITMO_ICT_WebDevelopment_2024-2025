import React from "react";
import Button from "react-bootstrap/Button";
import { useNavigate, useParams } from "react-router-dom";
import useUser from "../../hooks/useUser";

function Header({ returnButton }) {
  const navigate = useNavigate();
  const { setToken, token } = useUser();

  const onLogout = () => {
    setToken("");
    navigate("login");
  };

  const onReturn = () => {
    navigate("/");
  };

  return (
    <header>
      <div className="container header" style={{display: 'flex', alignItems: "center", justifyContent: "space-between", margin: "30px 0px"}}>
          <div class="header-logo" style={{fontWeight: '900', fontSize: '40px'}}>
            📚 SCHOOL APP
          </div>
          <div class="header-buttons">
          {returnButton ? <Button
              variant="outline-dark"
              className="logout-button"
              onClick={() => onReturn()}
            >
              ↩️ Return
            </Button> : ""}
            <Button
              variant="outline-danger"
              className="logout-button"
              onClick={() => onLogout()}
              style={{marginLeft: "20px"}}
            >
              ↪️ Logout
            </Button>
          </div>
      </div>
    </header>
  );
}

export default Header;