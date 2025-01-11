import { useContext } from "react";
import UserContext from "../context/UserProvider";

function useUser() {
  return useContext(UserContext);
}

export default useUser;