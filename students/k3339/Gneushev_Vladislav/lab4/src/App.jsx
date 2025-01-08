import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';

import { Login } from './pages/auth/Login';
import { Register } from './pages/auth/Register';

import { DriversList } from './pages/drivers/DriversList';
import { DriverDetails } from './pages/drivers/DriverDetails';
import { AddDriver } from './pages/drivers/AddDriver';

import { BusesList } from './pages/buses/BusesList';
import { AddBus } from './pages/buses/AddBus';

import { RoutesList } from './pages/routes/RoutesList';
import { AddRoute } from './pages/routes/AddRoute';

import { AssignmentsList } from './pages/assignments/AssignmentsList';
import { AddAssignment } from './pages/assignments/AddAssignment';

import { Profile } from './pages/profile/Profile';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/drivers" element={<DriversList />} />
          <Route path="/drivers/:id" element={<DriverDetails />} />
          <Route path="/drivers/add" element={<AddDriver />} />

          <Route path="/buses" element={<BusesList />} />
          <Route path="/buses/add" element={<AddBus />} />

          <Route path="/routes" element={<RoutesList />} />
          <Route path="/routes/add" element={<AddRoute />} />

          <Route path="/assignments" element={<AssignmentsList />} />
          <Route path="/assignments/add" element={<AddAssignment />} />

          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App; 