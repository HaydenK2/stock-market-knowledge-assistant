import axios from 'axios';

// create instance of axios with base URL
const api = axios.create({
    baseURL:  import.meta.env.VITE_API_URL || "http://localhost:8000"
})

// Export the Axios Instance
export default api;