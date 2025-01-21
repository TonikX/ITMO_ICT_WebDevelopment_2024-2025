import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './components/Auth/Login';
import Dashboard from "./pages/Dashboard";
import Register from './components/Auth/Register';
import Header from './components/layout/Header';
import PrivateRoute from './components/PrivateRoute';

import EditorList from './pages/editors/EditorList';
import EditorForm from './pages/editors/EditorForm';
import EditorDetail from './pages/editors/EditorDetail';

import NewspaperList from './pages/newspapers/NewspaperList';
import NewspaperForm from './pages/newspapers/NewspaperForm';
import NewspaperDetail from './pages/newspapers/NewspaperDetail';

import PrintShopList from './pages/printshops/PrintShopList';
import PrintShopForm from './pages/printshops/PrintShopForm';
import PrintShopDetail from './pages/printshops/PrintShopDetail';

import PostOfficeList from './pages/postoffices/PostOfficeList';
import PostOfficeForm from './pages/postoffices/PostOfficeForm';
import PostOfficeDetail from './pages/postoffices/PostOfficeDetail';

import DeliveryList from "./pages/deliveries/DeliveryList";
import DeliveryForm from "./pages/deliveries/DeliveryForm";
import DeliveryDetail from "./pages/deliveries/DeliveryDetail";

const App: React.FC = () => {
  return (
      <AuthProvider>

      <Router>
          <Header />
          <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/" element={<Navigate to="/editors" />} />

              <Route
                  path="/dashboard"
                  element={
                      <PrivateRoute>
                          <Dashboard />
                      </PrivateRoute>
                  }
              />

              <Route
                  path="/editors"
                  element={
                      <PrivateRoute>
                          <EditorList />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/editors/create"
                  element={
                      <PrivateRoute>
                          <EditorForm />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/editors/:editorId"
                  element={
                      <PrivateRoute>
                          <EditorDetail />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/editors/:editorId/edit"
                  element={
                      <PrivateRoute>
                          <EditorForm />
                      </PrivateRoute>
                  }
              />

              <Route
                  path="/newspapers"
                  element={
                      <PrivateRoute>
                          <NewspaperList />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/newspapers/create"
                  element={
                      <PrivateRoute>
                          <NewspaperForm />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/newspapers/:newspaperId"
                  element={
                      <PrivateRoute>
                          <NewspaperDetail />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/newspapers/:newspaperId/edit"
                  element={
                      <PrivateRoute>
                          <NewspaperForm />
                      </PrivateRoute>
                  }
              />

              <Route
                  path="/printshops"
                  element={
                      <PrivateRoute>
                          <PrintShopList />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/printshops/create"
                  element={
                      <PrivateRoute>
                          <PrintShopForm />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/printshops/:printshopId"
                  element={
                      <PrivateRoute>
                          <PrintShopDetail />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/printshops/:printshopId/edit"
                  element={
                      <PrivateRoute>
                          <PrintShopForm />
                      </PrivateRoute>
                  }
              />

              <Route
                  path="/postoffices"
                  element={
                      <PrivateRoute>
                          <PostOfficeList />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/postoffices/create"
                  element={
                      <PrivateRoute>
                          <PostOfficeForm />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/postoffices/:postofficeId"
                  element={
                      <PrivateRoute>
                          <PostOfficeDetail />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/postoffices/:postofficeId/edit"
                  element={
                      <PrivateRoute>
                          <PostOfficeForm />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/deliveries"
                  element={
                      <PrivateRoute>
                          <DeliveryList />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/deliveries/create"
                  element={
                      <PrivateRoute>
                          <DeliveryForm />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/deliveries/:deliveryId"
                  element={
                      <PrivateRoute>
                          <DeliveryDetail />
                      </PrivateRoute>
                  }
              />
              <Route
                  path="/deliveries/:deliveryId/edit"
                  element={
                      <PrivateRoute>
                          <DeliveryForm />
                      </PrivateRoute>
                  }
              />
          </Routes>

      </Router>
      </AuthProvider>
  );
};

export default App;