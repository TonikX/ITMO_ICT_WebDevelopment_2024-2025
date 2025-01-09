<template>
  <div class="search-workouts">
    <div class="theme-switcher text-center mb-3">
      <i
        @click="toggleTheme"
        :class="['fas', theme === 'light' ? 'fa-sun' : 'fa-moon', 'icon-button']"
        aria-label="Switch Theme"
      ></i>
    </div>

    <h1 class="text-center mb-4 main_header" id="mainHeader">Find Your Perfect Workout</h1>

    <!-- Фильтрация тренировок -->
    <div class="row workout-filter">
      <div class="col-md-4 level">
        <label for="levelFilter" class="form-label">Level</label>
        <select v-model="filters.level" class="form-select" id="levelFilter">
          <option disabled value="">Choose level...</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>
      <div class="col-md-4 type">
        <label for="typeFilter" class="form-label">Type</label>
        <select v-model="filters.type" class="form-select" id="typeFilter">
          <option disabled value="">Choose type...</option>
          <option value="cardio">Cardio</option>
          <option value="strength">Strength</option>
        </select>
      </div>
      <div class="col-md-4 duration">
        <label for="durationFilter" class="form-label">Duration</label>
        <select v-model="filters.duration" class="form-select" id="durationFilter">
          <option disabled value="">Choose duration...</option>
          <option value="short">Less than 30 mins</option>
          <option value="medium">30-60 mins</option>
          <option value="long">More than 60 mins</option>
        </select>
      </div>
    </div>

    <!-- Кнопка сброса фильтров -->
    <div class="text-center">
      <button @click="resetFilters" class="btn btn-secondary mb-4">Reset Filters</button>
    </div>

    <h2 id="workoutResultsTitle" class="visually-hidden">Workout Search Results</h2>

    <!-- Карточки тренировок -->
    <section aria-labelledby="workoutResultsTitle">
      <div class="row">
        <div
          v-for="(workout, index) in filteredWorkouts"
          :key="index"
          class="col-md-4"
        >
          <div class="card" role="region" aria-labelledby="workout1Title" aria-describedby="workout1Description">
            <img src="../pictures/workout1.jpg" class="card-img-top" alt="Workout Image" />
            <div class="card-body">
              <h5 class="card-title">{{ workout.title }}</h5>
              <p class="card-text">{{ workout.description }}</p>
              <p><strong>Type:</strong> {{ workout.type }} | <strong>Level:</strong> {{ workout.level }} | <strong>Duration:</strong> {{ workout.duration }}</p>
              <router-link to="/workout" class="btn btn-primary" aria-label="Start Workout">Start</router-link>
              <div class="d-flex justify-content-center mt-2">
                <button @click="saveWorkout(workout)" class="btn btn-primary save-button me-2">Save Workout</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Всплывающее окно для сохранения тренировки -->
    <div class="modal fade" id="savedModal" tabindex="-1" aria-labelledby="savedModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="savedModalLabel">Saved to Profile</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">Your workout has been saved to your profile.</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>


    <div class="text-center mt-4">
  <router-link to="/acc" class="btn btn-secondary">Back to Profile</router-link>
</div>
  </div>
</template>

<script>
import axios from 'axios';
import { TokenStore } from '@/stores/TokenStore.js';

export default {
  data() {
    return {
      theme: 'light',
      filters: {
        level: '',
        type: '',
        duration: '',
      },
      workouts: [],
      savedWorkouts: [],
    };
  },
  computed: {
    filteredWorkouts() {
      return this.workouts.filter(workout => {
        const workoutDurationInMinutes = this.convertDurationToMinutes(workout.duration);
        return (
          (!this.filters.level || workout.level === this.filters.level) &&
          (!this.filters.type || workout.type === this.filters.type) &&
          (!this.filters.duration ||
            (this.filters.duration === 'short' && workoutDurationInMinutes < 30) ||
            (this.filters.duration === 'medium' && workoutDurationInMinutes >= 30 && workoutDurationInMinutes <= 60) ||
            (this.filters.duration === 'long' && workoutDurationInMinutes > 60))
        );
      });
    },
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      document.documentElement.classList.toggle('blue-theme', this.theme === 'dark');
    },
    getUserId() {
    const userId = tokenStore.userId;
  },
  saveWorkout(workout) {
    const tokenStore = TokenStore();
    const userId = tokenStore.userId;

    const workoutData = {
      user: userId,
      workout: workout.id,
      scheduled_date: new Date().toISOString().split('T')[0]
    };

    axios.post('http://127.0.0.1:8000/app/workout-plans/create/', workoutData, {
      headers: {
        'Content-Type': 'application/json',
         Authorization: `Bearer ${tokenStore.token}`,
      }
    })
      .then(response => {
        console.log('Workout saved:', response.data);
        alert('Workout has been saved to your profile!');
      })
      .catch(error => {
        console.error('Error saving workout:', error);
        alert('Failed to save workout');
      });
  },
    resetFilters() {
      this.filters.level = '';
      this.filters.type = '';
      this.filters.duration = '';
    },
    async fetchWorkouts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/app/workouts/');
        this.workouts = response.data;
      } catch (error) {
        console.error('Error fetching workouts:', error);
      }
    },
    convertDurationToMinutes(duration) {
      const [hours, minutes] = duration.split(':').map(Number);
      return hours * 60 + minutes;
    },
  },
  created() {
    this.fetchWorkouts();
  },
};
</script>

<style scoped>
:root {
    --background-color: #fbeaff;
    --text-color: #333;
    --card-background: #fff;
    --heading-color: #6a0dad;
    --button-background: #ff85c0;
    --button-border: #ff85c0;
}

/* Альтернативная голубая тема */
.blue-theme {
    --background-color: #e0f7fa;
    --text-color: #333;
    --card-background: #ffffff;
    --heading-color: #00796b;
    --button-background: #00acc1;
    --button-border: #00acc1;
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
    margin: 0;
    font-family: Arial, sans-serif;
}

.search-workouts {
    padding: 20px;
}

.card {
    margin-bottom: 20px;
    background-color: var(--card-background);
    border-radius: 15px;
}

.card-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.save-button, .btn-primary {
    width: 150px;
}

.d-flex {
    display: flex;
}

.justify-content-center {
    justify-content: center;
}

.mt-2 {
    margin-top: 10px;
}

.workout-filter {
    margin-bottom: 30px;
}

.form-select {
    background-color: #f3e5f5;
    color: var(--text-color);
    border-radius: 10px;
}

.form-label {
    color: var(--heading-color);
}

.btn-primary {
    background-color: var(--button-background);
    border-color: var(--button-border);
    color: var(--text-color);
}

h1 {
    color: var(--heading-color);
}

.navigation-buttons {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
}

.icon-button {
    font-size: 2rem;
    padding: 15px;
    border: none;
    background: none;
    cursor: pointer;
    transition: transform 0.3s ease;
    color: #333;
}

.icon-button:hover {
    transform: scale(1.1);
    color: #000;
}

.theme-switcher i {
    font-size: 30px;
    cursor: pointer;
}

.btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
    color: #fff;
}
#savedModal .modal-content {
    background-color: var(--card-background);
    color: var(--text-color);
}
</style>
