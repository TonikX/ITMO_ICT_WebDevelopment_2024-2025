<template>
  <tr>
    <td>{{ workout.title }}</td>
    <td>{{ workout.type }}</td>
    <td>{{ workout.duration }}</td>
    <td>{{ workout.isCompleted ? "Yes" : "No" }}</td>
    <td class="button-container">
      <button @click="startWorkout" class="btn btn-warning">Start Workout</button>
      <button @click="$emit('delete', workout.id)" class="btn btn-danger">Delete</button>
    </td>
  </tr>
</template>

<script>
export default {
  name: "WorkoutCard",
  props: {
    workout: Object,
  },
  methods: {
    startWorkout() {
      const confirmed = window.confirm("This workout will be marked as completed.");
      if (confirmed) {
        this.$emit("start", this.workout);
      }
    },
  },
};
</script>

<style scoped>
.button-container {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.btn {
  width: 60%;
}
</style>
