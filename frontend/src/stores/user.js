import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
  const token = ref(sessionStorage.getItem('token') || '');
  const username = ref(JSON.parse(sessionStorage.getItem('user'))?.username || '');
  const role = ref(sessionStorage.getItem('user_type') || '');

  const setToken = (newToken) => {
    token.value = newToken;
    sessionStorage.setItem('token', newToken);
  };

  const setUsername = (newUsername) => {
    username.value = newUsername;
    sessionStorage.setItem('user', JSON.stringify({ username: newUsername }));
  };

  const setRole = (newRole) => {
    role.value = newRole;
    sessionStorage.setItem('user_type', newRole);
  };

  const logout = () => {
    token.value = '';
    username.value = '';
    role.value = '';
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    sessionStorage.removeItem('user_type');
  };

  return {
    token,
    username,
    role,
    setToken,
    setUsername,
    setRole,
    logout
  };
});
