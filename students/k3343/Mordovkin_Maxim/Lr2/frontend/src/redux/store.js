import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';

// Для поддержки Redux DevTools
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

// Инициализация состояния из localStorage, если токен существует
const initialState = {
    auth: {
        isAuthenticated: !!localStorage.getItem('token'),
        token: localStorage.getItem('token') || null,
        loading: false,
        error: null,
    }
};

const store = createStore(
    rootReducer,
    initialState,
    composeEnhancers(applyMiddleware(thunk))
);

export default store;
