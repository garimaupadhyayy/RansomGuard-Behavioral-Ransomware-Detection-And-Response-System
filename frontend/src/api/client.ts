import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const WS_URL = "ws://localhost:8000/api/ws/alerts";
