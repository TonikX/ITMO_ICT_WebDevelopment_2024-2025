import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Импорт FormsModule
import { TaskService } from '../../services/task.service';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, FormsModule], // Добавление FormsModule
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css'],
})
export class TaskListComponent {
  tasks: any[] = [];
  filter: string = ''; // Переменная для фильтрации

  constructor(private taskService: TaskService) {
    this.loadTasks();
  }

  loadTasks() {
    this.taskService.getTasks().subscribe((data) => {
      this.tasks = data;
    });
  }

  // Пример фильтрации
  get filteredTasks() {
    return this.tasks.filter((task) =>
      task.title.toLowerCase().includes(this.filter.toLowerCase())
    );
  }
}
