import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';
import api from '../services/api';

const HomePage = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    activeUsers: 0,
    newUsersThisMonth: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      // Fetch users and calculate stats
      const response = await api.get('/users');
      const users = response.data;
      
      const now = new Date();
      const thisMonth = now.getMonth();
      const thisYear = now.getFullYear();
      
      setStats({
        totalUsers: users.length,
        activeUsers: users.filter(user => user.isActive !== false).length,
        newUsersThisMonth: users.filter(user => {
          const createdDate = new Date(user.createdAt);
          return createdDate.getMonth() === thisMonth && 
                 createdDate.getFullYear() === thisYear;
        }).length
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="home-page">
      <div className="welcome-section">
        <h1>Welcome to User Management System</h1>
        <p>Manage your users efficiently with our comprehensive dashboard</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-number">{stats.totalUsers}</div>
          <div className="stat-label">Total Users</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.activeUsers}</div>
          <div className="stat-label">Active Users</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.newUsersThisMonth}</div>
          <div className="stat-label">New This Month</div>
        </div>
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <Link to="/users" className="btn btn-primary">
            View All Users
          </Link>
          <Link to="/users/new" className="btn btn-primary">
            Add New User
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;