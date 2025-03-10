import React, { useState, useEffect } from "react";
import { FaPlus } from "react-icons/fa";
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
        const response = await fetch("http://localhost:8000/todolist/get_user_tasks/", {
          credentials: 'include'
        });
        if (response.ok) {
          const data = await response.json();
          setTasks(data);
        } else if (response.status === 401) {
          setError("unauthorized");
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
          credentials: 'include'
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

  const handleCheck = async (taskUuid) => {
    const updatedTasks = tasks.map((task) =>
      task.uuid === taskUuid ? { ...task, is_done: !task.is_done } : task
    );
    setTasks(updatedTasks);
    try {
      const response = await fetch("http://localhost:8000/todolist/taskDone/", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ uuid: taskUuid, is_done: updatedTasks.find((task) => task.uuid === taskUuid).is_done }),
        credentials: 'include'
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
          credentials: 'include'
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
          onClick={() => window.location.href = "http://localhost:5173/login/"}
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
              className={`note-text ${task.is_done ? "line-through" : ""}`}>
              {task.description}
            </span>
            )}
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
    </div>
  );
};

export default TodoList;
