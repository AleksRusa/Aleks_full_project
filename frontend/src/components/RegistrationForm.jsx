import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; // Добавим импорт Link
import './RegistrationForm.css';

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    age: '',
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validatePassword = (password) => {
    const minLength = 6;
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    return password.length >= minLength && hasLetter && hasNumber;
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.first_name || formData.first_name.length < 2 || formData.first_name.length > 50) {
      newErrors.first_name = 'First name must be 2-50 characters';
    }

    if (!formData.last_name || formData.last_name.length < 2 || formData.last_name.length > 50) {
      newErrors.last_name = 'Last name must be 2-50 characters';
    }

    const age = parseInt(formData.age);
    if (isNaN(age) || age < 0 || age > 100) {
      newErrors.age = 'Age must be between 0 and 100';
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

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
        first_name: '',
        last_name: '',
        age: '',
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
        {/* First Name */}
        <div className={`form-group ${errors.first_name ? 'error-border' : ''}`}>
          <label>First Name:</label>
          <input 
            type="text" 
            name="first_name" 
            value={formData.first_name}
            onChange={handleChange}
          />
          {errors.first_name && <span className="error">{errors.first_name}</span>}
        </div>

        {/* Last Name */}
        <div className={`form-group ${errors.last_name ? 'error-border' : ''}`}>
          <label>Last Name:</label>
          <input 
            type="text" 
            name="last_name" 
            value={formData.last_name}
            onChange={handleChange}
          />
          {errors.last_name && <span className="error">{errors.last_name}</span>}
        </div>

        {/* Age */}
        <div className={`form-group ${errors.age ? 'error-border' : ''}`}>
          <label>Age:</label>
          <input 
            type="number" 
            name="age" 
            value={formData.age}
            onChange={handleChange}
          />
          {errors.age && <span className="error">{errors.age}</span>}
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