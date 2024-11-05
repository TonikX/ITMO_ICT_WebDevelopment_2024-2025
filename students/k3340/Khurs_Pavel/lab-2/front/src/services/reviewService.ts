const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const reviewsService = {
  getAllReviews: async (id: string) => {
    const res = await fetch(`${API_URL}/reviews/tour/${id}`, {
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
