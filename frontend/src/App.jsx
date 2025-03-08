import { Routes, Route } from "react-router-dom";
import RegistrationForm from "./components/RegistrationForm";
import LoginForm from "./components/LoginForm";
import UserProfile from "./components/UserProfile";
import TodoList from "./components/TodoList";

function App() {
  return (
    <Routes>
      <Route path="/register" element={<RegistrationForm />} />
      <Route path="/login" element={<LoginForm />} />
      <Route path="/user/me" element={<UserProfile />} />
      <Route path="/todolist" element={<TodoList />} />
    </Routes>
  );
}

export default App;
