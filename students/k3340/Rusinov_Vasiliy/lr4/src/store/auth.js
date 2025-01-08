import { reactive } from 'vue';

export const authState = reactive({
  isLoggedIn: !!localStorage.getItem('token'),
});

export function login() {
  authState.isLoggedIn = true;
}

export function logout() {
  localStorage.removeItem('token');
  authState.isLoggedIn = false;
}