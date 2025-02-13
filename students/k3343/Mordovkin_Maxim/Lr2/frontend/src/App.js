import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import { useSelector } from 'react-redux';
import './App.css';

import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import StudentPage from './pages/StudentPage';
import TeacherPage from './pages/TeacherPage';

function App() {
    const isAuthenticated = useSelector(state => state.auth.isAuthenticated);
    const role = useSelector(state => state.auth.role);

    return (
        <Router>
            <div className="app-container">
                <Switch>
                    {/* Главная (если не залогинен) */}
                    <Route exact path="/">
                        {isAuthenticated ?
                            (role === 'Teacher' ? <Redirect to="/teacher" /> : <Redirect to="/student" />)
                            : <LoginForm />
                        }
                    </Route>

                    {/* Регистрация */}
                    <Route path="/register">
                        {isAuthenticated ? <Redirect to="/" /> : <RegisterForm />}
                    </Route>

                    {/* Страница студента */}
                    <Route path="/student">
                        {/* Если не залогинен, редиректим на "/", иначе StudentPage */}
                        {isAuthenticated ? <StudentPage /> : <Redirect to="/" />}
                    </Route>

                    {/* Страница учителя */}
                    <Route path="/teacher">
                        {isAuthenticated ? <TeacherPage /> : <Redirect to="/" />}
                    </Route>

                    {/* Любой другой путь */}
                    <Route path="*">
                        <Redirect to="/" />
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}

export default App;
