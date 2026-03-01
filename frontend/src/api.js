import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getProfessors = () => axios.get(`${API}/professors`);
export const getProfessor = (name) => axios.get(`${API}/professor/${name}`);
export const searchProf = (q) => axios.get(`${API}/search?q=${q}`);
