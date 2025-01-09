<template>
  <div class="container workout" id="main-content" role="main">
    <!-- Переключатель темы -->
    <div class="theme-switcher text-center mb-3">
      <i :class="themeIcon" class="icon-button" @click="toggleTheme" aria-label="Switch Theme"></i>
    </div>

    <header>
      <h1 class="text-center mb-4">{{ workoutTitle }}</h1>
    </header>

    <!-- Видео -->
    <section class="video-container mb-4" aria-label="Workout Video">
      <iframe
        :src="videoSrc"
        frameborder="0"
        allowfullscreen
        title="Workout Video"
        loading="lazy"
      ></iframe>
    </section>

    <!-- Описание тренировки -->
    <section class="card mb-4" aria-labelledby="workout-description">
      <div class="card-body">
        <h5 id="workout-description" class="card-title">Workout Description</h5>
        <p class="card-text">{{ workoutDescription }}</p>
      </div>
    </section>

    <!-- Инструкции -->
    <section class="card-instructions" aria-labelledby="instructions">
      <div class="card-body">
        <h5 id="instructions" class="card-title">Instructions</h5>
        <ol>
          <li v-for="(step, index) in instructions" :key="index">
            {{ step.text }}
            <ul v-if="step.exercises">
              <li v-for="(exercise, exIndex) in step.exercises" :key="exIndex">
                {{ exercise }}
              </li>
            </ul>
          </li>
        </ol>
      </div>
    </section>

    <div class="text-center mt-4">
      <router-link to="/search" class="btn btn-primary" aria-label="Back to workout search page">
        Back to Workout Search
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      theme: 'light',
      workoutTitle: 'Beginner Cardio Workout',
      videoSrc: 'https://www.youtube.com/embed/fUJjsUn9bCo',
      workoutDescription:
        'This beginner cardio workout is designed to improve your endurance and burn calories. It consists of a series of exercises that will get your heart rate up and help you lose weight effectively.',
      instructions: [
        { text: 'Start with a 5-minute warm-up (jog in place).' },
        {
          text: 'Perform each exercise for 30 seconds:',
          exercises: ['Jumping Jacks', 'High Knees', 'Burpees', 'Mountain Climbers'],
        },
        { text: 'Rest for 1 minute after completing the circuit.' },
        { text: 'Repeat the circuit 3 times.' },
        { text: 'Cool down with stretching exercises for 5-10 minutes.' },
      ],
    };
  },
  computed: {
    themeIcon() {
      return this.theme === 'light' ? 'fas fa-sun' : 'fas fa-moon';
    },
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      document.body.className = this.theme;
    },
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

.workout {
    padding: 20px;
}

.video-container {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
}

.video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.card-instructions {
    background-color: var(--card-background);
    border-radius: 15px;
    margin-bottom: 20px;
    padding: 15px;
}

h1, .card-title {
    color: var(--heading-color);
}

.btn-primary {
    background-color: var(--button-background);
    border-color: var(--button-border);
    color: var(--text-color);
}

ol li {
    margin-bottom: 10px;
}

.theme-switcher i {
    font-size: 2rem;
    color: #000;
    transition: color 0.3s ease;
}

.theme-switcher {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
    cursor: pointer;
}

.theme-switcher:hover i {
    color: #00796b;
}
</style>
