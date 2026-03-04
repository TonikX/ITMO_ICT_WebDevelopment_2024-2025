import http from "./http";

export const guestsApi = {
  list() {
    return http.get("guests/");
  },

  create(data) {
    return http.post("guests/", data);
  },
};