import React, { useState, useEffect } from "react";
import { FaPlus, FaTrash } from "react-icons/fa";
import { v4 as uuidv4 } from "uuid";
import { useNavigate } from "react-router-dom";
import "./TodoList.css";

const TodoList = () => {
  const [tasks, setTasks] = useState([]);
  const [input, setInput] = useState("");
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editedText, setEditedText] = useState("");
  const [timeoutId, setTimeoutId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        // Запрос на получение задач
        const response = await fetch("http://localhost:8000/todolist/get_user_tasks/", {
          credentials: "include",
        });
  
        // Если задача загрузилась успешно
        if (response.ok) {
          const data = await response.json();
          setTasks(data);
        } else if (response.status === 401) {
          // Если не авторизован, попытаться обновить токен
          const refreshResponse = await fetch("http://localhost:8000/user/refresh/", {
            credentials: "include",
          });
  
          // Если refresh токен успешен
          if (refreshResponse.ok) {
            // После успешного обновления токена снова запросить задачи
            const retryResponse = await fetch("http://localhost:8000/todolist/get_user_tasks/", {
              credentials: "include",
            });
  
            if (retryResponse.ok) {
              const retryData = await retryResponse.json();
              setTasks(retryData);
            } else {
              setError("Ошибка при загрузке задач");
            }
          } else {
            setError("unauthorized");
          }
        } else {
          setError("Ошибка при загрузке задач");
        }
      } catch (error) {
        setError("Ошибка сети");
      } finally {
        setLoading(false);
      }
    };
  
    fetchTasks();
  }, [navigate]);
  

  const addTask = async () => {
    if (input.trim()) {
      const newTask = { uuid: uuidv4(), description: input.trim(), is_done: false };
      setTasks([...tasks, newTask]);
      setInput("");
      try {
        const response = await fetch("http://localhost:8000/todolist/createTask/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(newTask),
          credentials: "include",
        });

        if (response.status === 401) {
          setError("unauthorized");
        } else if (response.ok) {
          const data = await response.json();
          console.log(data.message);
        } else {
          console.error("Ошибка при добавлении задачи:", response.statusText);
        }
      } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
      }
    }
  };

  const handleDeleteUser = async () => {
    const userPassword = prompt("Введите пароль для подтверждения удаления аккаунта:");
    if (!userPassword) return;
  
    try {
      const response = await fetch("http://localhost:8000/user/delete_user/", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ password: userPassword }), // Передача пароля в теле запроса
      });
  
      if (response.ok) {
        alert("Аккаунт удалён");
        window.location.href = "/login";
      } else {
        console.error("Ошибка при удалении аккаунта");
      }
    } catch {
      console.error("Ошибка сети при удалении аккаунта");
    }
  };
  

  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:8000/user/logout/", {
        method: "POST",
        credentials: "include",
      });
      if (response.ok) {
        alert("Вы вышли из системы");
        window.location.href = "/login";
      } else {
        console.error("Ошибка при выходе из системы");
      }
    } catch {
      console.error("Ошибка сети при выходе из системы");
    }
  };


  const handleCheck = async (taskUuid) => {
    const updatedTasks = tasks.map((task) =>
      task.uuid === taskUuid ? { ...task, is_done: !task.is_done } : task
    );
    setTasks(updatedTasks);
    try {
      const response = await fetch("http://localhost:8000/todolist/taskDone/", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          uuid: taskUuid,
          is_done: updatedTasks.find((task) => task.uuid === taskUuid).is_done,
        }),
        credentials: "include",
      });
      if (response.status === 401) {
        setError("unauthorized");
      } else if (!response.ok) {
        console.error("Ошибка при обновлении статуса задачи:", response.statusText);
      }
    } catch (error) {
      console.error("Ошибка при выполнении запроса:", error);
    }
  };

  const handleDelete = async (taskUuid) => {
  try {
    const response = await fetch(`http://localhost:8000/todolist/deleteTask/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json", // Указываем тип данных
      },
      credentials: "include",
      body: JSON.stringify({ uuid: taskUuid }), // Передаем uuid в теле запроса
    });

    if (response.status === 401) {
      setError("unauthorized");
    } else if (response.ok) {
      setTasks(tasks.filter((task) => task.uuid !== taskUuid));
    } else {
      console.error("Ошибка при удалении задачи:", response.statusText);
    }
  } catch (error) {
    console.error("Ошибка при выполнении запроса:", error);
  }
};

  const handleEditClick = (task) => {
    setEditingTaskId(task.uuid);
    setEditedText(task.description);
  };

  const handleSaveEdit = async (taskUuid) => {
    if (editedText.trim()) {
      const updatedTasks = tasks.map((task) =>
        task.uuid === taskUuid ? { ...task, description: editedText.trim() } : task
      );
      setTasks(updatedTasks);
      setEditingTaskId(null);
      setEditedText("");
      try {
        const response = await fetch("http://localhost:8000/todolist/updateTask/", {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ uuid: taskUuid, description: editedText.trim() }),
          credentials: "include",
        });
        if (response.status === 401) {
          setError("unauthorized");
        } else if (!response.ok) {
          console.error("Ошибка при обновлении задачи:", response.statusText);
        }
      } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
      }
    }
  };

  const handleTextChange = (taskUuid, newText) => {
    setEditedText(newText);
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    const newTimeoutId = setTimeout(() => {
      handleSaveEdit(taskUuid);
    }, 500);
    setTimeoutId(newTimeoutId);
  };

  if (loading) return <div>Загрузка...</div>;

  if (error === "unauthorized") {
    return (
      <div className="login-message">
        <p>Чтобы просматривать и редактировать заметки, пожалуйста, войдите в аккаунт.</p>
        <button
          onClick={() => (window.location.href = "http://localhost/login/")}
          className="login-button"
        >
          Войти
        </button>
      </div>
    );
  }

  if (error) return <div>{error}</div>;

  return (
    <div className="notes-container">
      <h1 className="notes-title">Заметки</h1>
      <div className="notes-list">
        {tasks.map((task) => (
          <div key={task.uuid} className="note-item">
            <input
              type="checkbox"
              checked={task.is_done}
              onChange={() => handleCheck(task.uuid)}
              className="note-checkbox"
            />
            {editingTaskId === task.uuid ? (
              <input
                type="text"
                value={editedText}
                onChange={(e) => handleTextChange(task.uuid, e.target.value)}
                className="note-edit-input"
                autoFocus
              />
            ) : (
              <span
                onClick={() => handleEditClick(task)}
                className={`note-text ${task.is_done ? "line-through" : ""}`}
              >
                {task.description}
              </span>
            )}
            <button className="delete-button" onClick={() => handleDelete(task.uuid)}>
              <FaTrash />
            </button>
          </div>
        ))}
        <div className="new-note">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addTask()}
            className="note-input"
            placeholder="Новая заметка..."
          />
          <button onClick={addTask} className="add-note-button">
            <FaPlus />
          </button>
        </div>
      </div>
      <div className="user-actions">
        <button className="logout-button" onClick={handleLogout}>Выйти</button>
        <button className="delete-user-button" onClick={handleDeleteUser}>Удалить аккаунт</button>
      </div>
    </div>
  );
};

export default TodoList;
