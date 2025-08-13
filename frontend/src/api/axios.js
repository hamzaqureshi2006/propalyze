import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/api", // Django backend URL
  withCredentials: true, // Send cookies with every request
  headers: {
    "Content-Type": "application/json",
  },
});

// Optional: Add interceptors for request/response
axiosInstance.interceptors.request.use(
  (config) => {
    // Example: attach auth token from localStorage if not using cookies
    // const token = localStorage.getItem("access_token");
    // if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    // You can handle token refresh here if needed
    return Promise.reject(error);
  }
);

export default axiosInstance;
