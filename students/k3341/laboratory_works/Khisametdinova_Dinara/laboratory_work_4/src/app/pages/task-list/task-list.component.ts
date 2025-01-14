import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TaskService } from '../../services/task.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css'],
})
export class TaskListComponent {
  tasks: any[] = [];
  filter: string = '';
  isTeacher: boolean = false;
  currentUser: any = null;
  selectedCreatorId: number | null = null;
  creators: any[] = []; 

  newTask = {
    title: '',
    description: '',
  };

  editingTask: any = null;
  editingCriteria: any[] = [];
  editingOptions: any[] = [];

  constructor(private taskService: TaskService, private authService: AuthService) {
    this.currentUser = this.authService.getCurrentUser();
    this.isTeacher = this.currentUser?.role === 'teacher';

    if (this.isTeacher) {
      this.loadTasks();
      this.loadCreators();
    } else {
      this.loadTasksForStudents();
      this.loadCreators();
    }
  }

  loadTasks() {
    this.taskService.getTasks().subscribe({
      next: (data) => {
        this.tasks = data;
      },
      error: (err) => console.error('Error loading tasks:', err),
    });
  }

  loadTasksForStudents() {
    this.taskService.getTasksForStudents().subscribe({
      next: (data) => {
        this.tasks = data;
      },
      error: (err) => console.error('Error loading tasks for students:', err),
    });
  }

  loadCreators() {
    this.taskService.getCreators().subscribe({
      next: (data) => {
        this.creators = data;
      },
      error: (err) => console.error('Error loading creators:', err),
    });
  }

  filterTasksByCreator(creatorId: number | null) {
    if (creatorId === null) {
      this.isTeacher ? this.loadTasks() : this.loadTasksForStudents();
    } else {
      const filterMethod = this.isTeacher
        ? this.taskService.getTasksByCreator
        : this.taskService.getTasksByCreatorStudents;

      filterMethod.call(this.taskService, creatorId).subscribe({
        next: (data) => {
          this.tasks = data;
        },
        error: (err) => console.error('Error filtering tasks by creator:', err),
      });
    }
  }

  get filteredTasks() {
    return this.tasks.filter((task) =>
      task.title.toLowerCase().includes(this.filter.toLowerCase())
    );
  }

  createTask() {
    if (!this.newTask.title || !this.newTask.description) {
      alert('Please fill in all fields.');
      return;
    }
    const newTaskPayload = {
      ...this.newTask,
      criterion: this.editingCriteria,
      options: this.editingOptions,
    };
    this.taskService.createTask(newTaskPayload).subscribe({
      next: () => {
        this.loadTasks();
        this.newTask = { title: '', description: '' };
        this.editingCriteria = [];
        this.editingOptions = [];
      },
      error: (err) => console.error('Error creating task:', err),
    });
  }

  editTask(task: any) {
    if (task.creator.id !== this.currentUser.id) {
      alert("You don't have permission to edit this task.");
      return;
    }
    this.editingTask = { ...task };
    this.editingCriteria = task.criterion ? [...task.criterion] : [];
    this.editingOptions = task.options ? [...task.options] : [];
  }

  saveTask() {
    if (!this.editingTask.title || !this.editingTask.description) {
      alert('Please fill in all fields.');
      return;
    }
    const updatedTask = {
      ...this.editingTask,
      criterion: this.editingCriteria,
      options: this.editingOptions,
    };

    this.taskService.updateTask(this.editingTask.id, updatedTask).subscribe({
      next: () => {
        this.loadTasks();
        this.cancelEdit();
      },
      error: (err) => console.error('Error updating task:', err),
    });
  }

  deleteTask(taskId: number) {
    const taskToDelete = this.tasks.find((task) => task.id === taskId);
    if (taskToDelete?.creator.id !== this.currentUser.id) {
      alert("You don't have permission to delete this task.");
      return;
    }
    if (confirm('Are you sure you want to delete this task?')) {
      this.taskService.deleteTask(taskId).subscribe({
        next: () => this.loadTasks(),
        error: (err) => console.error('Error deleting task:', err),
      });
    }
  }

  cancelEdit() {
    this.editingTask = null;
  }

  addCriterion() {
    this.editingCriteria.push({ name: '', description: '', task: this.editingTask?.id || null });
  }

  removeCriterion(index: number) {
    this.editingCriteria.splice(index, 1);
  }

  addOption() {
    this.editingOptions.push({ content: '', task: this.editingTask?.id || null });
  }

  removeOption(index: number) {
    this.editingOptions.splice(index, 1);
  }
}
