import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import userService from '../services/userService';

function UserForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;
  
  const [formData, setFormData] = useState({
    name: '',
    email: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});

  useEffect(() => {
    if (isEdit) {
      fetchUser();
    }
  }, [id]);

  const fetchUser = async () => {
    try {
      setLoading(true);
      const user = await userService.getUserById(id);
      setFormData({
        name: user.name,
        email: user.email
      });
    } catch (error) {
      setError(`Failed to load user: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.name.trim()) {
      errors.name = 'Name is required';
    } else if (formData.name.trim().length > 100) {
      errors.name = 'Name must be less than 100 characters';
    }
    
    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Invalid email format';
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear validation error when user starts typing
    if (validationErrors[name]) {
      setValidationErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      if (isEdit) {
        await userService.updateUser(id, formData);
      } else {
        await userService.createUser(formData);
      }
      navigate('/users');
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/users');
  };

  if (loading && isEdit) {
    return (
      <div className="user-form-container">
        <div className="loading">Loading user data...</div>
      </div>
    );
  }

  return (
    <div className="user-form-container">
      <header className="App-header">
        <h1>{isEdit ? 'Edit User' : 'Create New User'}</h1>
        <p className="subtitle">{isEdit ? 'Update user information' : 'Add a new user to the system'}</p>
      </header>
      
      <main className="App-main">
        <form onSubmit={handleSubmit} className="user-form">
          {error && (
            <div className="error-message">{error}</div>
          )}
          
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={validationErrors.name ? 'error' : ''}
              disabled={loading}
            />
            {validationErrors.name && (
              <span className="field-error">{validationErrors.name}</span>
            )}
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={validationErrors.email ? 'error' : ''}
              disabled={loading}
            />
            {validationErrors.email && (
              <span className="field-error">{validationErrors.email}</span>
            )}
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Saving...' : (isEdit ? 'Update User' : 'Create User')}
            </button>
            <button 
              type="button" 
              onClick={handleCancel}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default UserForm;