import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './UserProfile.css'; // Импортируем стили

const UserProfile = () => {
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/user/me', {
                    withCredentials: true,
                });
                setUserData(response.data);
            } catch (err) {
                setError('Не удалось загрузить данные пользователя');
                console.error(err);
            }
        };

        fetchUserData();
    }, []);

    if (error) {
        return <div className="error">{error}</div>;
    }

    if (!userData) {
        return <div className="loading">Загрузка...</div>;
    }

    return (
        <div className="user-profile">
            <h2>Информация о пользователе</h2>
            <p><strong>Имя:</strong> {userData.first_name}</p>
            <p><strong>Фамилия:</strong> {userData.last_name}</p>
            <p><strong>Возраст:</strong> {userData.age}</p>
            <p><strong>Email:</strong> {userData.email}</p>
        </div>
    );
};

export default UserProfile;