import React, { useState, useEffect } from 'react';

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('/api/users');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setUsers(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return <div className="user-list-container loading">Loading users...</div>;
  }

  if (error) {
    return <div className="user-list-container error">Error: {error}</div>;
  }

  return (
    <div className="user-list-container">
      <h2>Mock Users</h2>
      {users.length > 0 ? (
        <div className="users-grid">
          {users.map(user => (
            <div key={user.id} className="user-card">
              <div className="user-id">#{user.id}</div>
              <div className="user-name">{user.name}</div>
              <div className="user-email">{user.email}</div>
            </div>
          ))}
        </div>
      ) : (
        <p className="no-users">No users found.</p>
      )}
    </div>
  );
}

export default UserList;