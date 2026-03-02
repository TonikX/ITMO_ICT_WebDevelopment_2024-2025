import { http } from "./http";

export function getTasks() {
  return http.get("/api/tasks/");
}

export function createTask(payload) {
  return http.post("/api/tasks/", payload);
}

export function deleteTask(id) {
  return http.delete(`/api/tasks/${id}/`);
}

export function updateTask(id, payload) {
  return http.patch(`/api/tasks/${id}/`, payload);
}


export function getTasksFull() {
  return http.get("/api/tasks/full/");
}
