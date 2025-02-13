import axios from 'axios';

// Установим базовый путь на WildFly-сервер
axios.defaults.baseURL = 'http://localhost:8080/backend_war';

// Регистрация пользователя
// Пример (authAction.js)
export const register = (username, password, role, classNumber) => async dispatch => {
    dispatch({ type: 'REGISTER_REQUEST' });
    try {
        const data = {
            username,
            password,
            role
        };
        // Если Student — добавляем classNumber
        if (role === 'Student') {
            data.classNumber = classNumber;
        }

        const response = await axios.post('/api/users/register', data);
        if (response.status === 201) {
            dispatch({ type: 'REGISTER_SUCCESS' });
        }
    } catch (error) {
        dispatch({
            type: 'REGISTER_FAILURE',
            payload: {
                error: error.response?.data?.message || 'Registration failed'
            }
        });
    }
};


// Вход пользователя (логин)
export const login = (username, password, role) => async dispatch => {
    dispatch({ type: 'LOGIN_REQUEST' });
    try {
        const response = await axios.post('/api/users/login', {
            username,
            password
        });
        if (response.status === 200) {
            const { token, role } = response.data;
            localStorage.setItem('token', token);
            localStorage.setItem('role', role);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            dispatch({
                type: 'LOGIN_SUCCESS',
                payload: { token, role }
            });
        }
    } catch (error) {
        dispatch({
            type: 'LOGIN_FAILURE',
            payload: {
                error: error.response?.data?.message || 'Login failed'
            }
        });
    }
};
