import axios from "axios";

const API = "http://127.0.0.1:8000";

// ========= BASIC API CALLS =========
export const getProfessors = () => axios.get(`${API}/professors`);
export const getProfessor = (name) => axios.get(`${API}/professor/${name}`);
export const searchProf = (q) => axios.get(`${API}/search?q=${q}`);

// ========= TREND ANALYSIS =========
export const getProfessorTrend = (name) => axios.get(`${API}/professor/${name}/trend`);
export const predictProfessorRating = (name, periods = 5) =>
  axios.get(`${API}/professor/${name}/predict?periods=${periods}`);

// ========= COMPARISON =========
export const compareProfessors = (names) => {
  const namesStr = Array.isArray(names) ? names.join(",") : names;
  return axios.get(`${API}/professors/compare?names=${namesStr}`);
};

export const compareProfessorsPost = (professorList) =>
  axios.post(`${API}/professors/compare`, { professors: professorList });

// ========= TOP PROFESSORS =========
export const getTopProfessors = (by = "rating", n = 10, minRatings = 5) =>
  axios.get(`${API}/professors/top?by=${by}&n=${n}&min_ratings=${minRatings}`);

// ========= HEALTH =========
export const healthCheck = () => axios.get(`${API}/health`);
