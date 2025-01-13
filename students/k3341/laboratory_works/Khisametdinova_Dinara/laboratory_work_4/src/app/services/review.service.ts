import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ReviewService {
  private baseUrl = 'http://127.0.0.1:8000/peer';

  constructor(private http: HttpClient) {}

  // Получить список рецензий
  getReviews(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/reviews/`);
  }

  // Добавить новую рецензию
  createReview(review: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/reviews/`, review);
  }

  // Обновить рецензию по ID
  updateReview(id: number, review: any): Observable<any> {
    return this.http.put<any>(`${this.baseUrl}/reviews/${id}/`, review);
  }

  // Удалить рецензию по ID
  deleteReview(id: number): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/reviews/${id}/`);
  }

  // Получить все задачи
  getAllTasks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/tasks/for-students/`);
  }

  // Получить детали задачи
  getTaskDetails(taskId: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/tasks/${taskId}/details/`);
  }

  // Получить submissions по задаче
  getSubmissionsByTask(taskId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/submissions/?task=${taskId}`);
  }
}
