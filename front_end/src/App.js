import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';  // Ensure BrowserRouter is imported correctly
import Login from "./components/Login";
import Home from "./components/Home";
import EditorPage from './components/EditorPage';

import './index.css'; 

function App() {
   return (
      <div className="App">
       <Router>
       <Routes>
             <Route exact path="/" element={<Login />}></Route>
             <Route exact path="/redirect" element={<Home />}></Route>
             <Route exact path="/editor" element={<EditorPage />}></Route>
        </Routes>
       </Router>
      </div>
  );
}

export default App;