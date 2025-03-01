import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Импортируем useNavigate
import './LoginForm.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate(); // Инициализируем navigate

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/user/login/', formData);
      const token = response.data.access_token;

      // Сохраняем токен в localStorage или cookies
      localStorage.setItem('token', token);

      // Перенаправляем пользователя на защищенную страницу
      navigate('/dashboard', { replace: true }); // Используем navigate вместо window.location.href
    } catch (error) {
      console.log('Login error:', error.response);

      if (
        error.response &&
        error.response.data &&
        error.response.data.detail === "Incorrect username or password"
      ) {
        setErrors({ login: "Неверный email или пароль" });
      } else {
        alert('Ошибка при входе: ' + error.message);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <div className={`form-group ${errors.email ? 'error-border' : ''}`}>
        <label>Email:</label>
        <input 
          type="email" 
          name="email" 
          value={formData.email}
          onChange={handleChange}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div className={`form-group ${errors.password ? 'error-border' : ''}`}>
        <label>Password:</label>
        <input 
          type="password" 
          name="password" 
          value={formData.password}
          onChange={handleChange}
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>

      {errors.login && <span className="error">{errors.login}</span>}

      <button type="submit" className="submit-btn">Login</button>
    </form>
  );
};

export default LoginForm;