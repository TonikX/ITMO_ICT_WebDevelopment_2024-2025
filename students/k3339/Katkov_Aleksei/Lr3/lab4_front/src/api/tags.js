import { http } from "./http";

export function getTags() {
  return http.get("/api/tags/");
}

export function createTag(payload) {
  return http.post("/api/tags/", payload);
}
