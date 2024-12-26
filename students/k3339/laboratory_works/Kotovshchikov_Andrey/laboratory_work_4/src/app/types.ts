interface IPerson {
  first_name: string;
  last_name: string;
}

export interface ISignUpRequest extends IPerson {
  email: string;
  password: string;
}

export interface ISignInRequest {
  email: string;
  password: string;
}

export interface IGuest extends IPerson {
  patronymic: string | null;
  passport: string;
  city: string;
}

export interface ISchedule {
  week_day: Weekdays;
  floor: number;
}

export interface IAddGuestRequest extends IGuest {}

export interface ICreateBookingRequest {
  guest_passport: string;
  check_out_date: string;
}

export interface IHireEmployeeRequest extends IPerson {
  patronymic: string | null;
  hire_date: string;
}

export interface IUpdateEmployeeRequest extends IHireEmployeeRequest {
  dismissal_date: string | null;
}

export interface IEmployee extends IUpdateEmployeeRequest {
  id: number;
}

export interface IEmployeeDetail extends IEmployee {
  schedule: ISchedule[];
}

export type Weekdays = 'пн' | 'вт' | 'ср' | 'чт' | 'пт' | 'сб' | 'вс';

export interface IRoom {
  id: number;
  label: string;
  phone: string;
  floor: number;
  room_type: {
    beds: number;
    price_per_day: number;
  };
}

export interface IReport {
  guests_per_room: { [key: string]: number };
  rooms_per_floor: { [key: string]: number };
  profit_per_room: { [key: string]: number };
  total_profit: number;
}
