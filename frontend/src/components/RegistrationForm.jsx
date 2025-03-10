import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; // Добавим импорт Link
import './RegistrationForm.css';

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  // Валидация password: минимальная длина, буквы и цифры
  const validatePassword = (password) => {
    const minLength = 6;
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    return password.length >= minLength && hasLetter && hasNumber;
  };

  // Валидация username: только буквы
  const validateUsername = (username) => {
    return /^[a-zA-Z]+$/.test(username); // Только буквы
  };

  const validate = () => {
    const newErrors = {};

    // Валидация username
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (!validateUsername(formData.username)) {
      newErrors.username = 'Username must contain only letters';
    }

    // Валидация email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    // Валидация password
    if (!validatePassword(formData.password)) {
      newErrors.password = 'Password must be at least 6 characters with letters and numbers';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      const response = await axios.post(
        "http://localhost:8000/user/register/", 
        formData,
        { withCredentials: true }
      );
      alert('Регистрация прошла успешно!');

      // Очистка формы
      setFormData({
        username: '',
        email: '',
        password: ''
      });

      // Перенаправление на страницу авторизации через React Router
      navigate('/login', { replace: true });
    } catch (error) {
      console.log('Server error:', error.response);

      if (
        error.response &&
        error.response.data &&
        error.response.data.detail === "Пользователь с таким email уже зарегистрирован"
      ) {
        setErrors(prevErrors => ({
          ...prevErrors,
          email: "Аккаунт с такой почтой уже зарегистрирован"
        }));
      } else {
        alert('Ошибка при регистрации: ' + error.message);
      }
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="registration-container"> {/* Добавляем контейнер для центрирования */}
      <h2>Регистрация</h2> {/* Добавляем заголовок "Регистрация" */}
      <form onSubmit={handleSubmit} className="registration-form">
        {/* Username */}
        <div className={`form-group ${errors.username ? 'error-border' : ''}`}>
          <label>Username:</label>
          <input 
            type="text" 
            name="username" 
            value={formData.username}
            onChange={handleChange}
          />
          {errors.username && <span className="error">{errors.username}</span>}
        </div>

        {/* Email */}
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

        {/* Password */}
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

        <button type="submit" className="submit-btn">Register</button>

        {/* Блок ссылки "Уже есть аккаунт?" */}
        <div className="login-link">
          Уже есть аккаунт?{' '}
          <Link to="/login" className="link">
            Войдите
          </Link>
        </div>
      </form>
    </div>
  );
};

export default RegistrationForm;
