import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ReviewService {
  private baseUrl = 'http://127.0.0.1:8000/peer/reviews';

  constructor(private http: HttpClient) {}

  // Получить список рецензий
  getReviews(): Observable<any[]> {
    return this.http.get<any[]>(this.baseUrl);
  }

  // Добавить новую рецензию
  createReview(review: any): Observable<any> {
    return this.http.post<any>(this.baseUrl, review);
  }

  // Обновить рецензию по ID
  updateReview(id: number, review: any): Observable<any> {
    return this.http.put<any>(`${this.baseUrl}/${id}`, review);
  }

  // Удалить рецензию по ID
  deleteReview(id: number): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/${id}`);
  }
}
