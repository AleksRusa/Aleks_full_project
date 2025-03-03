import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import UserProfile from './components/UserProfile';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/user/me" element={<UserProfile />} />
      </Routes>
    </Router>
  );
}

export default App;