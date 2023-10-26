import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import HomePage from "./HomePage";
import 'tailwindcss/tailwind.css';

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* <Route path="/models" element={<MyModel />} /> */}
        </Routes>
      </Router>
  );
}

export default App;
