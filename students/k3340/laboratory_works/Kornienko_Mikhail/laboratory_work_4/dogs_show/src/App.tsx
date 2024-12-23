import React from 'react';
import {BrowserRouter, Routes, Route, NavLink, Navigate, useNavigate} from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import ProtectedPage from './pages/ProtectedPage';
import 'antd/dist/reset.css';
import OwnersList from "./pages/OwnersList.tsx";
import OwnerForm from "./pages/OwnerForm.tsx";
import DogsList from "./pages/DogsList.tsx";
import DogForm from "./pages/DogForm.tsx";
import {Avatar, Dropdown, Layout, Menu} from 'antd';
import ShowsList from "./pages/ShowsList.tsx";
import ShowForm from "./pages/ShowForm.tsx";
import ExpertsList from "./pages/ExpertsList.tsx";
import ExpertForm from "./pages/ExpertForm.tsx";
import AppHeader from "./components/Header.tsx";
import DogDetail from "./pages/DogDetail.tsx";
import ShowDetail from "./pages/ShowDetail.tsx";
import Dashboard from "./pages/Dashboard.tsx";
const { Content } = Layout;


const App: React.FC = () => {

    return (
        <AuthProvider>
            <BrowserRouter>
                <AppHeader />

                <Content style={{ padding: '24px' }}>
                    <Routes>
                        <Route path="/login" element={<LoginPage />} />

                        <Route element={<ProtectedRoute />}>
                            <Route path="/" element={<Dashboard />} />

                            <Route path="/owners" element={<OwnersList />} />
                            <Route path="/owners/new" element={<OwnerForm />} />
                            <Route path="/owners/edit/:id" element={<OwnerForm />} />

                            <Route path="/dogs" element={<DogsList />} />
                            <Route path="/dogs/new" element={<DogForm />} />
                            <Route path="/dogs/edit/:id" element={<DogForm />} />
                            <Route path="/dogs/:id" element={<DogDetail />} />

                            <Route path="/shows" element={<ShowsList />} />
                            <Route path="/shows/new" element={<ShowForm />} />
                            <Route path="/shows/edit/:id" element={<ShowForm />} />
                            <Route path="/shows/:id" element={<ShowDetail />} />

                            <Route path="/experts" element={<ExpertsList />} />
                            <Route path="/experts/new" element={<ExpertForm />} />
                            <Route path="/experts/edit/:id" element={<ExpertForm />} />
                        </Route>
                    </Routes>
                </Content>
            </BrowserRouter>
        </AuthProvider>
    );
};

export default App;
