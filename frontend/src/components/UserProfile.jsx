import React, { useEffect, useState } from "react";
import axios from "axios";
import "./UserProfile.css"; // Стили

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Запрос на получение данных пользователя
        const response = await axios.get("http://backend:8000/user/me", {
          withCredentials: true,
        });
        setUserData(response.data);
      } catch (err) {
        console.error("Ошибка при загрузке данных:", err.response);
        if (err.response?.status === 401) {
          try {
            // Если 401, пробуем обновить токены
            await axios.get("http://backend:8000/user/refresh/", {
              withCredentials: true,
            });

            // После успешного обновления токенов пробуем снова получить данные пользователя
            const retryResponse = await axios.get("http://backend:8000/user/me", {
              withCredentials: true,
            });
            setUserData(retryResponse.data);
          } catch (refreshError) {
            console.error("Ошибка при обновлении токена:", refreshError.response);
            setError("Сессия истекла. Пожалуйста, войдите заново.");
          }
        } else {
          setError("Не удалось загрузить данные пользователя.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <div className="loading">Загрузка...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div>
      <div className="user-profile">
        <h2>Информация о пользователе</h2>
        <p><strong>Имя пользователя:</strong> {userData.username}</p>
        <p><strong>Email:</strong> {userData.email}</p>
      </div>

      <div className="notes-message">
        <p>Перейти к заметкам</p>
        <button
          onClick={() => window.location.href = "http://172.20.10.2:3000/todolist/"}
          className="notes-button"
        >
          Заметки
        </button>
      </div>
    </div>
  );
};

export default UserProfile;
