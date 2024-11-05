const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const toursService = {
  getAllTours: async () => {
    const res = await fetch(`${API_URL}/tours`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.message);
    }

    return res.json();
  },
  getTourById: async (id: string) => {
    const res = await fetch(`${API_URL}/tours/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.message);
    }

    return res.json();
  },
};
