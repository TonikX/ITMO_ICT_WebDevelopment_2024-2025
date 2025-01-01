import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SubmissionService {
  private baseUrl = 'http://127.0.0.1:8000/peer/submissions';

  constructor(private http: HttpClient) {}

  // Метод для получения списка Submissions
  getSubmissions(): Observable<any[]> {
    return this.http.get<any[]>(this.baseUrl);
  }

  // Метод для создания Submission
  createSubmission(submission: any): Observable<any> {
    return this.http.post(this.baseUrl, submission);
  }

  // Метод для обновления Submission
  updateSubmission(id: number, submission: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/${id}`, submission);
  }

  // Метод для удаления Submission
  deleteSubmission(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }
}
