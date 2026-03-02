import { http } from "./http";

export function getCategories() {
  return http.get("/api/categories/");
}

export function createCategory(payload) {
  return http.post("/api/categories/", payload);
}

export function deleteCategory(id) {
  return http.delete(`/api/categories/${id}/`);
}

export function getCategoriesFull() {
  return http.get("/api/categories/full/");
}
