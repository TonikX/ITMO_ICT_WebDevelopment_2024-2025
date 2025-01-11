import { createContext, useState } from "react";

const UserContext = createContext({
  token: "",
  setToken: () => {},
});

export const UserProvider = ({ children }) => {
  const [token, setToken] = useState("");

  return (
    <UserContext.Provider value={{ token, setToken }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;