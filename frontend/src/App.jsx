import { Navigate, Route, Routes } from "react-router-dom";
import { session } from "./api/client";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import StudentHome from "./pages/StudentHome";
import TeacherHome from "./pages/TeacherHome";
import AdminHome from "./pages/AdminHome";
import QuizList from "./pages/QuizList";
import TakeQuiz from "./pages/TakeQuiz";
import Practice from "./pages/Practice";
import Performance from "./pages/Performance";
import QuestionBank from "./pages/QuestionBank";
import CreateQuiz from "./pages/CreateQuiz";
import Insights from "./pages/Insights";
import People from "./pages/People";

function RequireAuth({ children }) {
  if (!session().token) return <Navigate to="/" replace />;
  return children;
}

function HomeSwitch() {
  const role = session().role;
  if (role === "admin") return <AdminHome />;
  if (role === "teacher") return <TeacherHome />;
  return <StudentHome />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/app" element={<RequireAuth><Layout /></RequireAuth>}>
        <Route index element={<HomeSwitch />} />
        <Route path="quizzes" element={<QuizList />} />
        <Route path="quizzes/new" element={<CreateQuiz />} />
        <Route path="quizzes/:id" element={<TakeQuiz />} />
        <Route path="practice" element={<Practice />} />
        <Route path="performance" element={<Performance />} />
        <Route path="questions" element={<QuestionBank />} />
        <Route path="insights" element={<Insights />} />
        <Route path="people" element={<People />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
