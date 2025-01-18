import {ref, computed} from 'vue';

export const TokenRef = ref(localStorage.getItem('AuthToken'));

export const IsAuthenticated = computed(() => !!TokenRef.value);

export const SetAuthToken = (token) => {
    TokenRef.value = token;
    localStorage.setItem('AuthToken', token);
};

export const ClearAuthToken = () => {
    TokenRef.value = null;
    localStorage.removeItem('AuthToken');
};
