import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import HomePage from './components/HomePage';
import UserList from './components/UserList';
import UserDetail from './components/UserDetail';
import UserForm from './components/UserForm';
import SwaggerPage from './components/SwaggerPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <nav className="nav-menu">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/users" className="nav-link">Users</Link>
          <Link to="/swagger" className="nav-link">API Documentation</Link>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/users" element={<UserList />} />
            <Route path="/users/new" element={<UserForm />} />
            <Route path="/users/:id" element={<UserDetail />} />
            <Route path="/users/:id/edit" element={<UserForm />} />
            <Route path="/swagger" element={<SwaggerPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;