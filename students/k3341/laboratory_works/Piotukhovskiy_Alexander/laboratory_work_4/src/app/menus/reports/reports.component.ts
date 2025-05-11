import {Component, OnInit} from '@angular/core';
import {environment} from '../../environment';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-reports',
  imports: [
    CommonModule,
    FormsModule,
  ],
  templateUrl: './reports.component.html',
  styleUrl: './reports.component.css',
})
export class ReportsComponent implements OnInit {
  appName: string = environment.appName;
  username: string | null = null;
  quarters: number[] = [1, 2, 3, 4];
  years: number[] = [];
  selectedQuarter: number | null = null;
  selectedYear: number | null = null;
  report: any = null;

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
    this.username = localStorage.getItem('username');
    this.loadYears();
  }

  loadYears() {
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= currentYear - 10; year--) {
      this.years.push(year);
    }
  }

  fetchReport() {
    if (!this.selectedQuarter || !this.selectedYear) {
      alert('Пожалуйста, выберите квартал и год.');
      return;
    }

    const params = {
      quarter: this.selectedQuarter.toString(),
      year: this.selectedYear.toString(),
    };

    this.http
      .get(`${environment.apiUrl}/hotel/reports/quarterly`, {params})
      .subscribe({
        next: (data: any) => {
          this.report = data;
        },
        error: (err) => {
          console.error('Ошибка получения отчёта:', err);
        },
      });
  }

  numWord(value: number, words: [string, string, string]): string {
    let num = value % 100;
    if (num > 19) {
      num = num % 10;
    }
    switch (num) {
      case 1:
        return words[0];
      case 2:
      case 3:
      case 4:
        return words[1];
      default:
        return words[2];
    }
  }


  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }

  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }
}
