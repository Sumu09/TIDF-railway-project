// JWT Authentication Utility
// Handles JWT token validation and API authorization

const JWT_AUTH = {
  // Check if user is authenticated
  isAuthenticated() {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.log("JWT_AUTH: No token found");
      return false;
    }

    // Check if token is expired (basic check)
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      const currentTime = Math.floor(Date.now() / 1000);

      console.log("JWT_AUTH: Token payload:", payload);
      console.log(
        "JWT_AUTH: Current time:",
        currentTime,
        "Token exp:",
        payload.exp
      );

      if (payload.exp && payload.exp < currentTime) {
        console.log("JWT_AUTH: Token expired");
        localStorage.removeItem("authToken");
        return false;
      }

      console.log("JWT_AUTH: Token is valid");
      return true;
    } catch (error) {
      console.log("JWT_AUTH: Token decode error:", error);
      localStorage.removeItem("authToken");
      return false;
    }
  },

  // Get the JWT token
  getToken() {
    return localStorage.getItem("authToken");
  },

  // Set the JWT token
  setToken(token) {
    localStorage.setItem("authToken", token);
  },

  // Remove the JWT token
  removeToken() {
    localStorage.removeItem("authToken");
  },

  // Redirect to login if not authenticated
  requireAuth(loginUrl = "/") {
    if (!this.isAuthenticated()) {
      window.location.href = loginUrl;
      return false;
    }
    return true;
  },

  // Get authorization headers for API calls
  getAuthHeaders() {
    const token = this.getToken();
    return token
      ? {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        }
      : {
          "Content-Type": "application/json",
        };
  },

  // Make authenticated API call
  async fetchWithAuth(url, options = {}) {
    const headers = this.getAuthHeaders();

    const config = {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      // If unauthorized, redirect to login
      if (response.status === 401) {
        this.removeToken();
        window.location.href = "/";
        return null;
      }

      return response;
    } catch (error) {
      console.error("API call failed:", error);
      throw error;
    }
  },

  // Logout user
  logout() {
    this.removeToken();
    window.location.href = "/";
  },
};

// Auto-redirect to login on page load if not authenticated (for protected pages)
function protectPage() {
  if (!JWT_AUTH.requireAuth()) {
    return false;
  }
  return true;
}
