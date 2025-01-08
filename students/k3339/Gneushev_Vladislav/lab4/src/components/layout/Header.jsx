import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

export const Header = () => {
  const { user, isAdmin } = useAuth();

  return (
    <header className="bg-blue-600 text-white">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-xl font-bold">
            Автобусный парк
          </Link>
          
          <div className="flex gap-4">
            {!user ? (
              <>
                <Link to="/login">Вход</Link>
                <Link to="/register">Регистрация</Link>
              </>
            ) : (
              <>
                {isAdmin && (
                  <>
                    <Link to="/drivers">Водители</Link>
                    <Link to="/buses">Автобусы</Link>
                    <Link to="/routes">Маршруты</Link>
                    <Link to="/assignments">Назначения</Link>
                  </>
                )}
                <Link to="/profile">Профиль</Link>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}; 