import api from "./api";

export async function registerUser(name, email, password) {
    const response = await api.post("/auth/register", {
        name: name,
        email: email,
        password: password,
    });

    return response.data;
}

export async function loginUser(email, password) {
    const response = await api.post("/auth/login", {
        email: email,
        password: password,
    });

    return response.data;
}

export function saveToken(token) {
    if (token) {
        localStorage.setItem("smartnotes-token", token);
    }
}

export function getToken() {
    return localStorage.getItem("smartnotes-token");
}

export function logoutUser() {
    localStorage.removeItem("smartnotes-token");
}

export function isLoggedIn() {
    return localStorage.getItem("smartnotes-token") !== null;
}