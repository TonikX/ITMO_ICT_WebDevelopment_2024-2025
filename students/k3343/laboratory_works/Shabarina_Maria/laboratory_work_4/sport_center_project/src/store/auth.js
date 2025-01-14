import { reactive } from 'vue';

const authState = reactive({
  token: localStorage.getItem('authToken') || null,
  isAuthenticated: !!localStorage.getItem('authToken'),
});

const login = (token) => {
  authState.token = token;
  authState.isAuthenticated = true;
  localStorage.setItem('authToken', token);
};

const logout = () => {
  authState.token = null;
  authState.isAuthenticated = false;
  localStorage.removeItem('authToken');
};

export default { authState, login, logout };
