import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SubmissionService {
  private baseUrl = 'http://127.0.0.1:8000/peer';

  constructor(private http: HttpClient) {}

  getSubmissions(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/submissions/`);
  }

  createSubmission(submission: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/submissions/`, submission);
  }

  updateSubmission(id: number, submission: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/submissions/${id}/`, submission);
  }

  deleteSubmission(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/submissions/${id}/`);
  }

  getTaskDetails(taskId: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/tasks/${taskId}/details`);
  }
  getAllTasks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/tasks/for-students/`);
  }
  getSubmissionsByTask(taskId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/submissions/?task=${taskId}`);
  }  
}
