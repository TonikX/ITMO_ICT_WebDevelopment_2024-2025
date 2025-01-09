<template>
  <div>
    <ProgressTracker
      :totalWorkouts="workouts.length"
      :workoutsCompleted="workouts.filter(workout => workout.isCompleted).length"
    />

    <div class="card" aria-labelledby="workoutSchedule">
      <div class="card-body">
        <h2 class="card-workout-title" id="workoutSchedule">Your Saved Workouts</h2>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Workout Name</th>
              <th scope="col">Type</th>
              <th scope="col">Duration</th>
              <th scope="col">Is Completed</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="workouts.length === 0">
              <td colspan="5" class="text-center">No saved workouts yet</td>
            </tr>
            <tr v-for="workout in workouts" :key="workout.id">
              <td>{{ workout.title }}</td>
              <td>{{ workout.type }}</td>
              <td>{{ workout.duration }}</td>
              <td>{{ workout.isCompleted ? 'Yes' : 'No' }}</td>
              <td>
                <button class="btn btn-primary btn-sm" @click="handleStartWorkout(workout)">
                  Start Workout
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteWorkout(workout.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import ProgressTracker from './ProgressTracker.vue';

export default {
  name: "SavedWorkouts",
  components: { ProgressTracker },
  props: {
    userId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      workouts: [],
    };
  },
  methods: {
    async fetchSavedWorkouts() {
      try {
        const workoutPlansResponse = await fetch("http://127.0.0.1:8000/app/workout-plans/");
        const workoutPlans = await workoutPlansResponse.json();
        const userWorkoutPlans = workoutPlans.filter((plan) => plan.user === this.userId);

        const workoutsResponse = await fetch("http://127.0.0.1:8000/app/workouts/");
        const allWorkouts = await workoutsResponse.json();

        const userWorkouts = allWorkouts.filter((workout) =>
          userWorkoutPlans.some((plan) => plan.workout === workout.id)
        );

        const savedWorkouts = JSON.parse(localStorage.getItem("savedWorkouts")) || [];
        this.workouts = userWorkouts.map((workout) => {
          const savedWorkout = savedWorkouts.find((w) => w.id === workout.id);
          return {
            id: workout.id,
            title: workout.title,
            type: workout.type,
            duration: workout.duration,
            isCompleted: savedWorkout ? savedWorkout.isCompleted : false,
          };
        });

        localStorage.setItem("savedWorkouts", JSON.stringify(this.workouts));
      } catch (error) {
        console.error("Error fetching saved workouts:", error);
      }
    },
    handleStartWorkout(workout) {
      const confirmation = window.confirm('This workout will be marked as completed. Do you want to proceed?');

      if (confirmation) {
        // Обновляем состояние тренировки
        this.workouts = this.workouts.map((w) =>
          w.id === workout.id ? { ...w, isCompleted: true } : w
        );

        const updatedWorkouts = JSON.parse(localStorage.getItem("savedWorkouts")) || [];
        const syncedWorkouts = updatedWorkouts.map((w) =>
          w.id === workout.id ? { ...w, isCompleted: true } : w
        );
        localStorage.setItem("savedWorkouts", JSON.stringify(syncedWorkouts));

        // Сохраняем текущую тренировку и переходим на страницу тренировки
        localStorage.setItem("currentWorkout", JSON.stringify(workout));
        this.$router.push({ name: "Workout" });
      }
    },
    deleteWorkout(workoutId) {
      this.workouts = this.workouts.filter((workout) => workout.id !== workoutId);
      const updatedWorkouts = JSON.parse(localStorage.getItem("savedWorkouts")) || [];
      const filteredWorkouts = updatedWorkouts.filter((w) => w.id !== workoutId);
      localStorage.setItem("savedWorkouts", JSON.stringify(filteredWorkouts));
    },
  },
  mounted() {
    this.fetchSavedWorkouts();
  },
};
</script>
