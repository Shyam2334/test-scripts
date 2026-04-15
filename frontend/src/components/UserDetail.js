import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import './UserDetail.css';

const UserDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    fetchUser();
  }, [id]);

  const fetchUser = async () => {
    try {
      const response = await fetch(`/api/users/${id}`);
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      } else if (response.status === 404) {
        setError('User not found');
      } else {
        throw new Error('Failed to fetch user');
      }
    } catch (err) {
      setError('An error occurred while fetching user details');
      console.error('Error fetching user:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    setDeleteLoading(true);
    try {
      const response = await fetch(`/api/users/${id}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        navigate('/');
      } else {
        throw new Error('Failed to delete user');
      }
    } catch (err) {
      console.error('Error deleting user:', err);
      alert('Failed to delete user. Please try again.');
    } finally {
      setDeleteLoading(false);
      setShowDeleteModal(false);
    }
  };

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
      <div className="user-detail-container">
        <div className="user-detail-loading">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="user-detail-container">
        <div className="user-detail-error">
          <div className="user-detail-error-icon">⚠️</div>
          <p className="user-detail-error-message">{error}</p>
          <Link to="/" className="btn btn-primary">
            Back to Users
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="user-detail-container">
      <div className="user-detail-card">
        <div className="user-detail-header">
          <div className="user-detail-header-content">
            <h1 className="user-detail-title">
              <div className="user-detail-icon">
                {getInitials(user.name)}
              </div>
              {user.name}
            </h1>
            <p className="user-detail-subtitle">User Profile Details</p>
          </div>
        </div>
        
        <div className="user-detail-body">
          <div className="user-detail-section">
            <h2 className="user-detail-section-title">Contact Information</h2>
            <div className="user-detail-info">
              <div className="user-detail-field">
                <div className="user-detail-label">User ID</div>
                <div className="user-detail-value">#{user.id}</div>
              </div>
              <div className="user-detail-field">
                <div className="user-detail-label">Full Name</div>
                <div className="user-detail-value">{user.name}</div>
              </div>
              <div className="user-detail-field">
                <div className="user-detail-label">Email Address</div>
                <div className="user-detail-value">{user.email}</div>
              </div>
            </div>
          </div>
          
          <div className="user-detail-actions">
            <Link to="/" className="btn btn-secondary">
              Back to List
            </Link>
            <Link to={`/users/${id}/edit`} className="btn btn-warning btn-icon">
              <span>✏️</span>
              Edit User
            </Link>
            <button
              onClick={() => setShowDeleteModal(true)}
              className="btn btn-danger btn-icon"
            >
              <span>🗑️</span>
              Delete User
            </button>
          </div>
        </div>
      </div>
      
      {showDeleteModal && (
        <div className="delete-modal-overlay" onClick={() => setShowDeleteModal(false)}>
          <div className="delete-modal" onClick={(e) => e.stopPropagation()}>
            <div className="delete-modal-header">
              <h3>Confirm Deletion</h3>
            </div>
            <div className="delete-modal-body">
              <p>Are you sure you want to delete <strong>{user.name}</strong>?</p>
              <p>This action cannot be undone.</p>
            </div>
            <div className="delete-modal-actions">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="btn btn-secondary"
                disabled={deleteLoading}
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="btn btn-danger"
                disabled={deleteLoading}
              >
                {deleteLoading ? 'Deleting...' : 'Delete User'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserDetail;