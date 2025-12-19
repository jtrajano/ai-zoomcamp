// React import removed as it is not used directly and new JSX transform handles it
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { RoomView } from './views/RoomView';
import './index.css';

function App() {
  const generateRoomId = () => Math.random().toString(36).substring(2, 8);

  return (
    <Router>
      <Routes>
        <Route path="/room/:roomId" element={<RoomView />} />
        <Route path="/" element={<Navigate to={`/room/${generateRoomId()}`} replace />} />
      </Routes>
    </Router>
  );
}

export default App;
