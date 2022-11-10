import React from 'react';
import AppLayout from 'components/AppLayout';
import { Routes, Route } from 'react-router-dom';
import Login from 'pages/auth/Login';
import AccidentReconstruction from 'pages/solution/accident-reconstruction/Index';

const App: React.FC = () => (
  <div className='App'>
    <Routes>
      <Route path='/' element={<AppLayout />}>
        <Route path='/home' element={<div>Home</div>} />
        <Route
          path='/accident-reconstruction'
          element={<AccidentReconstruction />}
        />
      </Route>
      <Route path='/auth/login' element={<Login />} />
    </Routes>
  </div>
);

export default App;
