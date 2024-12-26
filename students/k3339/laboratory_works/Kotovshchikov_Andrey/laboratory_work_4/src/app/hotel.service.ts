import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {
  ICreateBookingRequest,
  IAddGuestRequest,
  IGuest,
  IHireEmployeeRequest,
  IRoom,
  IReport,
  IEmployee,
  ISchedule,
  IEmployeeDetail,
  IUpdateEmployeeRequest,
} from './types';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class HotelService {
  private readonly baseUrl: string = 'http://127.0.0.1:8000/hotel';

  constructor(private readonly http: HttpClient) {}

  getGuests() {
    const url = `${this.baseUrl}/guests/`;
    return this.http.get<{ guests: IGuest[] }>(url);
  }

  filterGuestsByCity(city: string) {
    const url = `${this.baseUrl}/guests/`;
    const queryParams = new HttpParams().set('city', city);
    return this.http.get<{ guests: IGuest[] }>(url, { params: queryParams });
  }

  getRooms() {
    const url = `${this.baseUrl}/rooms/`;
    return this.http.get<{ count: number; rooms: IRoom[] }>(url).pipe(
      map((response) => {
        return {
          rooms: response.rooms,
          total: response.count,
        };
      })
    );
  }

  getAvailableRooms() {
    const url = `${this.baseUrl}/rooms/`;
    const queryParams = new HttpParams().set('available', true);
    return this.http
      .get<{ count: number; rooms: IRoom[] }>(url, { params: queryParams })
      .pipe(
        map((response) => {
          return {
            rooms: response.rooms,
            total: response.count,
          };
        })
      );
  }

  getEmployees() {
    const url = `${this.baseUrl}/employees/`;
    return this.http.get<{ employees: IEmployee[] }>(url);
  }

  getEmployeeDetail(employeeId: number) {
    const url = `${this.baseUrl}/employees/${employeeId}/`;
    return this.http.get<IEmployeeDetail>(url);
  }

  addGuest(data: IAddGuestRequest) {
    const url = `${this.baseUrl}/guests/`;
    return this.http.post(url, data);
  }

  createBooking(roomId: number, data: ICreateBookingRequest) {
    const url = `${this.baseUrl}/rooms/${roomId}/booking/`;
    return this.http.post(url, data);
  }

  vacateRoom(roomId: number) {
    const url = `${this.baseUrl}/rooms/${roomId}/booking/`;
    return this.http.delete(url);
  }

  hireEmployee(data: IHireEmployeeRequest) {
    const url = `${this.baseUrl}/employees/`;
    return this.http.post(url, data);
  }

  updateEmployee(employeeId: number, data: IUpdateEmployeeRequest) {
    const url = `${this.baseUrl}/employees/${employeeId}/`;
    return this.http.put(url, data);
  }

  createEmployeeSchedule(employeeId: number, data: ISchedule) {
    const url = `${this.baseUrl}/employees/${employeeId}/schedule/`;
    return this.http.post(url, data);
  }

  resetEmployeeSchedule(employeeId: number) {
    const url = `${this.baseUrl}/employees/${employeeId}/schedule/reset/`;
    return this.http.delete(url);
  }

  generateReport(quarter: number) {
    const url = `${this.baseUrl}/reports/${quarter}/`;
    return this.http.get<IReport>(url);
  }
}
