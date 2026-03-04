import { http } from "./http";

export const roomsApi = {
  list() {
    return http.get("/rooms/");
  },

  // ВАЖНО: теперь принимает даты
  free(params = {}) {
    // params: { check_in: "YYYY-MM-DD", check_out: "YYYY-MM-DD" }
    return http.get("/rooms/free/", { params });
  },
};

