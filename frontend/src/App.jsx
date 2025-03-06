import { BrowserRouter } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import UserProfile from './components/UserProfile';
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/user/me" element={<UserProfile />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;