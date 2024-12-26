const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const reservationsService = {
  getAllReservations: async () => {
    const res = await fetch(`${API_URL}/reservations`, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.message);
    }

    return res.json();
  },
};
