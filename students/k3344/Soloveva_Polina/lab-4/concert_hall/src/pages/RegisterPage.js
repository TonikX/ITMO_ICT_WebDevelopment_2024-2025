import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/auth/register/', {
        username,
        email,
        password
      });
      setSuccess('Регистрация успешна! Теперь вы можете войти.');
      setError(null);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError('Ошибка регистрации. Возможно, имя пользователя уже занято.');
      setSuccess(null);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="card p-4 shadow" style={{ width: '300px' }}>
        <h2 className="text-center">Регистрация</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input className="form-control" type="text" placeholder="Имя пользователя" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div className="mb-3">
            <input className="form-control" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="mb-3">
            <input className="form-control" type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button className="btn btn-primary w-100" type="submit">Зарегистрироваться</button>
        </form>
        {error && <p className="text-danger text-center mt-2">{error}</p>}
        {success && <p className="text-success text-center mt-2">{success}</p>}
        <p className="text-center mt-3">Уже есть аккаунт? <Link to="/login">Войти</Link></p>
      </div>
    </div>
  );
};

export default RegisterPage;
