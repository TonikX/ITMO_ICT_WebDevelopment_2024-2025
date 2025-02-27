import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useHistory } from 'react-router-dom';
import { login } from '../redux/actions/authAction';
import InteractiveBackground from './InteractiveBackground';
import './css/AuthForms.css';

const LoginForm = () => {
    const dispatch = useDispatch();
    const history = useHistory();
    const auth = useSelector(state => state.auth);

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('Student'); // Значение роли по умолчанию
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            // Передаём роль вместе с логином и паролем
            await dispatch(login(username, password, role));
            history.push('/main');
        } catch (err) {
            setError(auth.error || 'Произошла ошибка при входе.');
        }
    };

    return (
        <div className="auth-container">
            <InteractiveBackground />
            <div className="auth-form-container">
                <div className="auth-form-content">
                    <h1>Вход</h1>
                    {error && <div className="error-message">{error}</div>}
                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-field">
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Логин"
                                required
                            />
                        </div>
                        <div className="form-field">
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Пароль"
                                required
                            />
                        </div>

                        <button type="submit" className="submit-button">
                            Войти
                        </button>
                    </form>
                    <p className="auth-link">
                        Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default LoginForm;
