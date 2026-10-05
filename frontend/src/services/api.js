import axios from "axios";

export const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:5000/api";

export const USE_MOCK_API =
    String(
        import.meta.env.VITE_USE_MOCK_API || "false"
    ) === "true";

const api = axios.create({
    baseURL: API_BASE_URL,

    // General requests
    timeout: 120000
});

api.interceptors.request.use(
    function(config) {

        const token =
            localStorage.getItem(
                "smartnotes-token"
            );

        if (token) {

            config.headers.Authorization =
                "Bearer " + token;
        }

        return config;
    },

    function(error) {

        return Promise.reject(error);
    }
);

api.interceptors.response.use(

    function(response) {

        return response;
    },

    function(error) {

        let message = "Request failed";

        if (error.code === "ECONNABORTED") {

            message =
                "The AI is taking longer than expected. Please wait and try again.";
        } else if (error.response) {

            if (error.response.data) {

                message =
                    error.response.data.message ||
                    error.response.data.error ||
                    message;
            }
        } else if (error.message) {

            message = error.message;
        }

        return Promise.reject(
            new Error(message)
        );
    }
);

export default api;