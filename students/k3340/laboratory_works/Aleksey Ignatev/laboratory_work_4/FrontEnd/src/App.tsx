import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import LoginPage from './pages/login/Login'
import Nav from './components/nav/Navigator'
import HomePage from './pages/home/HomePage'
import RegisterPage from './pages/reg/Register'
import { ToastContainer } from 'react-toastify'
import ResetPasswordPage from './pages/reset_password/ResetPasswordPage'
import ActivatePage from './pages/activate/ActivatePage'
import 'react-toastify/dist/ReactToastify.css'
import Dashboard from './pages/dashboard/Dashboard'
import NotFoundPage from './pages/notFound/NotFoundPage'
import ResetPasswordPageConfirm from './pages/reset_password_confirm/ResetPasswordPageConfirm'
import AnimalsPage from './pages/animals/Animals'
import DietsPage from './pages/diets/Diets'

function App() {
  return (
    <>
      <Router>
        <Nav />
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/register' element={<RegisterPage />} />
          <Route path='/reset-password' element={<ResetPasswordPage />} />
          <Route path='/activate/:uid/:token' element={<ActivatePage />} />
          <Route
            path='/password/reset/confirm/:uid/:token'
            element={<ResetPasswordPageConfirm />}
          />
          <Route path='/dashboard' element={<Dashboard />} />
          <Route path='/animals' element={<AnimalsPage />} />
          <Route path='/diets' element={<DietsPage />} />
          <Route path='*' element={<NotFoundPage />} />
        </Routes>
      </Router>
      <ToastContainer />
    </>
  )
}

export default App
