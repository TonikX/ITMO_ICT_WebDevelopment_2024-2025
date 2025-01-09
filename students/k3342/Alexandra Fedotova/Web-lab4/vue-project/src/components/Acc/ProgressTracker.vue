<template>
  <div class="card us_progress" aria-labelledby="progressTracking">
    <div class="card-body">
      <h2 class="card-title" id="progressTracking">Progress Tracking</h2>
      <div class="d-flex justify-content-center">
        <div class="circle-progress" aria-labelledby="workoutsCompleted">
          <svg viewBox="0 0 36 36">
            <circle class="bg-circle" cx="18" cy="18" r="16" fill="none" stroke-width="3"></circle>
            <circle
              class="main-circle-workouts"
              cx="18" cy="18" r="16" fill="none" stroke-width="3"
              :stroke-dasharray="workoutsProgress + ', 100'"
            ></circle>
            <text x="50%" y="50%" class="progress-text" text-anchor="middle" dy=".3em">
              {{ workoutsCompleted }}/{{ totalWorkouts }}
            </text>
          </svg>
          <p id="workoutsCompleted">Workouts Completed</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProgressTracker",
  props: {
    totalWorkouts: {
      type: Number,
      required: true,
    },
    workoutsCompleted: {
      type: Number,
      required: true,
    },
  },
  computed: {
    workoutsProgress() {
      return this.totalWorkouts > 0
        ? (this.workoutsCompleted / this.totalWorkouts) * 100
        : 0;
    },
  },
};
</script>
