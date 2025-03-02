import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import './LoginForm.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password) => {
    return password.length >= 6;
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.password.trim()) {
      newErrors.password = 'Password is required';
    } else if (!validatePassword(formData.password)) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      const response = await axios.post('http://127.0.0.1:8000/user/login/', formData);
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      navigate('/dashboard', { replace: true });
    } catch (error) {
      console.log('Login error:', error.response);

      if (error.response?.data?.detail) {
        switch (error.response.data.detail) {
          case "Incorrect username or password":
            setErrors(prev => ({ ...prev, login: "Неверный email или пароль" }));
            break;
          case "Пользователь не найден":
            setErrors(prev => ({ ...prev, userNotFound: "Вы не зарегистрированы" }));
            break;
          default:
            alert('Ошибка при входе: ' + error.message);
        }
      } else {
        alert('Ошибка при входе: ' + error.message);
      }
    }
  };

  return (
    <div className="login-container">
      <h2>Авторизация</h2>
      <form onSubmit={handleSubmit} className="login-form">
        {errors.login && <div className="form-error">{errors.login}</div>}
        {errors.userNotFound && <div className="form-error">{errors.userNotFound}</div>}

        <div className={`form-group ${errors.email ? 'error-border' : ''}`}>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
          {errors.email && <span className="error">{errors.email}</span>}
        </div>

        <div className={`form-group ${errors.password ? 'error-border' : ''}`}>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          />
          {errors.password && <span className="error">{errors.password}</span>}
        </div>

        <button type="submit" className="submit-btn">Войти</button>
        
        <div className="registration-link">
          Ещё нет аккаунта? 
          <Link to="/" className="link"> Зарегистрируйтесь </Link>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;