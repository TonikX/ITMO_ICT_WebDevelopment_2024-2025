import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class HomeService {
  private baseUrl = 'http://127.0.0.1:8000/peer';

  constructor(private http: HttpClient) {}

  getUploadedTasks(userId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/tasks?creator=${userId}`);
  }

  getUploadedSubmissions(userId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/submissions?creator=${userId}`);
  }

  getReviews(userId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/reviews?reviewer=${userId}`);
  }

  getTaskDetails(taskId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/tasks/${taskId}/details/`);
  }

  getSubmissionDetails(submissionId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/submissions/${submissionId}/`);
  }

  getReviewDetails(reviewId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/reviews/${reviewId}/`);
  }
}
