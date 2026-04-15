import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './UserList.css';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/users');
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      } else {
        throw new Error('Failed to fetch users');
      }
    } catch (err) {
      setError('Failed to load users. Please try again later.');
      console.error('Error fetching users:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  if (loading) {
    return (
      <div className="user-list-container">
        <div className="user-list-loading">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="user-list-container">
        <div className="user-list-error">
          <div className="error-icon">⚠️</div>
          <p className="error-message">{error}</p>
          <button onClick={fetchUsers} className="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="user-list-container">
      <div className="user-list-header">
        <div className="user-list-header-content">
          <h1 className="user-list-title">User Management</h1>
          <p className="user-list-subtitle">Manage your organization's users</p>
        </div>
        <Link to="/users/new" className="btn btn-primary btn-create">
          <span className="btn-icon">+</span>
          Create New User
        </Link>
      </div>

      <div className="user-list-controls">
        <div className="search-container">
          <input
            type="text"
            className="search-input"
            placeholder="Search by name or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <span className="search-icon">🔍</span>
        </div>
        <div className="user-count">
          {filteredUsers.length} {filteredUsers.length === 1 ? 'user' : 'users'} found
        </div>
      </div>

      {filteredUsers.length === 0 ? (
        <div className="user-list-empty">
          <div className="empty-icon">👥</div>
          <p className="empty-message">
            {searchTerm ? 'No users match your search.' : 'No users found.'}
          </p>
          {!searchTerm && (
            <Link to="/users/new" className="btn btn-primary">
              Create Your First User
            </Link>
          )}
        </div>
      ) : (
        <div className="user-list-grid">
          {filteredUsers.map(user => (
            <div key={user.id} className="user-card">
              <div className="user-card-header">
                <div className="user-avatar">
                  {getInitials(user.name)}
                </div>
                <div className="user-info">
                  <h3 className="user-name">{user.name}</h3>
                  <p className="user-email">{user.email}</p>
                </div>
              </div>
              <div className="user-card-footer">
                <span className="user-id">ID: #{user.id}</span>
                <div className="user-actions">
                  <Link 
                    to={`/users/${user.id}`} 
                    className="user-action-link"
                    title="View Details"
                  >
                    👁️
                  </Link>
                  <Link 
                    to={`/users/${user.id}/edit`} 
                    className="user-action-link"
                    title="Edit User"
                  >
                    ✏️
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UserList;