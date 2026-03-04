import { http } from "./http";

export const staysApi = {
  list() {
    return http.get("stays/");
  },

  create(payload) {
    // payload: {guest: guest_id, room: room_id, check_in: "YYYY-MM-DD", check_out?: null}
    return http.post("stays/", payload);
  },

  patch(id, payload) {
    return http.patch(`stays/${id}/`, payload);
  },
};