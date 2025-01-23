import React, { useState } from 'react';
import axios from 'axios';
import {Link, useNavigate} from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/auth/login/', { username, password });
      const response2 = await axios.post('http://localhost:8000/auth/token/token/login', { username, password });
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('token', response2.data.auth_token)
      console.log(response2)
      setError(null);
      navigate("/");
    } catch (err) {
      setError('Неверное имя пользователя или пароль');
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="card p-4 shadow" style={{width: '300px'}}>
        <h2 className="text-center">Вход</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input className="form-control" type="text" placeholder="Имя пользователя" value={username}
                   onChange={(e) => setUsername(e.target.value)}/>
          </div>
          <div className="mb-3">
            <input className="form-control" type="password" placeholder="Пароль" value={password}
                   onChange={(e) => setPassword(e.target.value)}/>
          </div>
          <button className="btn btn-primary w-100" type="submit">Войти</button>
        </form>
        {error && <p className="text-danger text-center mt-2">{error}</p>}
        <p className="text-center mt-3">Впервые здесь? <Link to="/register">Зарегистрироваться</Link></p>
      </div>
    </div>
  );
};

export default LoginPage;
