import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import userService from '../services/userService';

function UserDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUser();
  }, [id]);

  const fetchUser = async () => {
    try {
      setLoading(true);
      const userData = await userService.getUserById(id);
      setUser(userData);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete ${user.name}?`)) {
      try {
        await userService.deleteUser(id);
        navigate('/users');
      } catch (error) {
        setError(`Failed to delete user: ${error.message}`);
      }
    }
  };

  if (loading) {
    return (
      <div className="user-detail-container">
        <div className="loading">Loading user details...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="user-detail-container">
        <div className="error">Error: {error}</div>
        <Link to="/users" className="btn btn-secondary">Back to Users</Link>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="user-detail-container">
        <div className="error">User not found</div>
        <Link to="/users" className="btn btn-secondary">Back to Users</Link>
      </div>
    );
  }

  return (
    <div className="user-detail-container">
      <header className="App-header">
        <h1>User Details</h1>
        <p className="subtitle">View user information</p>
      </header>
      
      <main className="App-main">
        <div className="user-detail-card">
          <div className="user-detail-field">
            <label>ID:</label>
            <span>{user.id}</span>
          </div>
          
          <div className="user-detail-field">
            <label>Name:</label>
            <span>{user.name}</span>
          </div>
          
          <div className="user-detail-field">
            <label>Email:</label>
            <span>{user.email}</span>
          </div>
          
          {user.created_at && (
            <div className="user-detail-field">
              <label>Created:</label>
              <span>{new Date(user.created_at).toLocaleString()}</span>
            </div>
          )}
          
          <div className="user-detail-actions">
            <Link to={`/users/${id}/edit`} className="btn btn-primary">
              Edit
            </Link>
            <button onClick={handleDelete} className="btn btn-danger">
              Delete
            </button>
            <Link to="/users" className="btn btn-secondary">
              Back to List
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}

export default UserDetail;