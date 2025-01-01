import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TaskService {
  private baseUrl = 'http://127.0.0.1:8000/peer/tasks';

  constructor(private http: HttpClient) {}

  getTasks(): Observable<any[]> {
    return this.http.get<any[]>(this.baseUrl);
  }

  createTask(task: any): Observable<any> {
    return this.http.post(this.baseUrl, task);
  }

  updateTask(id: number, task: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/${id}`, task);
  }

  deleteTask(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }

  getAverageScore(taskId: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/${taskId}/average-score`);
  }

  getAverageScoreByUsername(username: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/average-score/${username}`);
  }  
}
