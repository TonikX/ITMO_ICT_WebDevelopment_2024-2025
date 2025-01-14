import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ReportService {
  private baseUrl = 'http://127.0.0.1:8000/peer';

  constructor(private http: HttpClient) {}

  getUploadedTasks(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/tasks/?creator=${userId}`);
  }

  getReviewedTasks(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/reviews/?user=${userId}`);
  }

  getAverageScoreByUsername(username: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/tasks/average-score/${username}/`);
  }

  getTaskStatistics(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/statistics/`);
  }  

  getPersonalStatistics(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/personal-statistics/`);
  }  
}
