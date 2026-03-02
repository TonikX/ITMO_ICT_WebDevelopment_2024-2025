import { ref } from "vue";

export const token = ref(localStorage.getItem("token") || "");

export function setToken(newToken) {
  token.value = newToken || "";
  if (token.value) localStorage.setItem("token", token.value);
  else localStorage.removeItem("token");
}
