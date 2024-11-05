export interface TravelAgencyData {
  name: string;
  id: number;
  contactInfo: string;
}

export interface TourData {
  title: string;
  description: string;
  id: number;
  startDate: string;
  endDate: string;
  paymentConditions: string;
  country: string;
  travelAgency: TravelAgencyData;
}

export interface ReviewData {
  comment: string;
  rating: number;
  tourDate: string;
  createdAt: string;
  user: {
    id: number;
    name: string;
    email: string;
    isBlocked: false;
  };
}
