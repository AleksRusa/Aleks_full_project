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
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch("http://localhost/todolist/get_user_tasks/", {
          credentials: 'include'
        });
        if (response.ok) {
          const data = await response.json();
          setTasks(data);
        } else if (response.status === 401) {
          navigate("/login");
        } else {
          console.error("Ошибка при загрузке задач:", response.statusText);
        }
      } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
      }
    };
    fetchTasks();
  }, [navigate]);

  const addTask = async () => {
    if (input.trim()) {
      const newTask = { id: uuidv4(), text: input.trim(), done: false };
      setTasks([...tasks, newTask]);
      setInput("");
      try {
        const response = await fetch("http://localhost/todolist/createTask/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ description: newTask.text }),
          credentials: 'include'
        });
        if (response.status === 401) {
          navigate("/login");
        } else if (!response.ok) {
          console.error("Ошибка при добавлении задачи:", response.statusText);
        }
      } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
      }
    }
  };

  const handleCheck = async (taskId) => {
    const updatedTasks = tasks.map((task) =>
      task.id === taskId ? { ...task, done: !task.done } : task
    );
    setTasks(updatedTasks);
    try {
      const response = await fetch("http://localhost/todolist/taskDone/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: taskId, done: updatedTasks.find((task) => task.id === taskId).done }),
        credentials: 'include'
      });
      if (response.status === 401) {
        navigate("/login");
      } else if (!response.ok) {
        console.error("Ошибка при обновлении статуса задачи:", response.statusText);
      }
    } catch (error) {
      console.error("Ошибка при выполнении запроса:", error);
    }
  };

  const handleEditClick = (task) => {
    setEditingTaskId(task.id);
    setEditedText(task.text);
  };

  const handleSaveEdit = async (taskId) => {
    if (editedText.trim()) {
      const updatedTasks = tasks.map((task) =>
        task.id === taskId ? { ...task, text: editedText.trim() } : task
      );
      setTasks(updatedTasks);
      setEditingTaskId(null);
      setEditedText("");
      try {
        const response = await fetch("http://localhost/todolist/updateTask/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: taskId, description: editedText.trim() }),
          credentials: 'include'
        });
        if (response.status === 401) {
          navigate("/login");
        } else if (!response.ok) {
          console.error("Ошибка при обновлении задачи:", response.statusText);
        }
      } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
      }
    }
  };

  const handleTextChange = (taskId, newText) => {
    setEditedText(newText);
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    const newTimeoutId = setTimeout(() => {
      handleSaveEdit(taskId);
    }, 500);
    setTimeoutId(newTimeoutId);
  };

  return (
    <div className="notes-container">
      <h1 className="notes-title">Заметки</h1>
      <div className="notes-list">
        {tasks.map((task) => (
          <div key={task.id} className="note-item">
            <input
              type="checkbox"
              checked={task.done}
              onChange={() => handleCheck(task.id)}
              className="note-checkbox"
            />
            {editingTaskId === task.id ? (
              <input
                type="text"
                value={editedText}
                onChange={(e) => handleTextChange(task.id, e.target.value)}
                className="note-edit-input"
                autoFocus
              />
            ) : (
              <span
                onClick={() => handleEditClick(task)}
                className={`note-text ${task.done ? "line-through" : ""}`}
              >
                {task.text}
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