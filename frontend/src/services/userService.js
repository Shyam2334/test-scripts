const API_BASE_URL = '/api';

class UserService {
  async getAllUsers() {
    try {
      const response = await fetch(`${API_BASE_URL}/users`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  }

  async getUserById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${id}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('User not found');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching user:', error);
      throw error;
    }
  }

  async createUser(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 400) {
          throw new Error(errorData.detail || 'Bad request');
        }
        if (response.status === 422) {
          throw new Error('Invalid user data');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  }

  async updateUser(id, userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 404) {
          throw new Error('User not found');
        }
        if (response.status === 400) {
          throw new Error(errorData.detail || 'Bad request');
        }
        if (response.status === 422) {
          throw new Error('Invalid user data');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error updating user:', error);
      throw error;
    }
  }

  async deleteUser(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${id}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('User not found');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('Error deleting user:', error);
      throw error;
    }
  }
}

export default new UserService();