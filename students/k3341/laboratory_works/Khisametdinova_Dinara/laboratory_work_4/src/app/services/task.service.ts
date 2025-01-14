import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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

  getTasksForStudents(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/for-students/`);
  }

  createTask(task: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/`, task, this.getHttpOptions());
  }

  updateTask(id: number, task: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/${id}/details/`, task, this.getHttpOptions());
  }

  deleteTask(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}/`, this.getHttpOptions());
  }

  getAverageScore(taskId: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/${taskId}/average-score`);
  }

  getAverageScoreByUsername(username: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/average-score/${username}`);
  }

  getTasksByCreator(creatorId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/?creator=${creatorId}`);
  }
  
  getTasksByCreatorStudents(creatorId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/for-students/?creator=${creatorId}`);
  }

  getCreators(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/peer/users/');
  }
  
  private getHttpOptions() {
    const token = localStorage.getItem('auth_token');
    return {
      headers: new HttpHeaders({
        Authorization: `Token ${token}`,
      }),
    };
  }
}
