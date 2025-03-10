<template>
  <div class="container mt-4">
    <h1>Progress Tracker</h1>
    <hr/>

    <form @submit.prevent="submitForm" class="mb-4">
      <div class="row g-3">
        <div class="col-md-4">
          <label for="date" class="form-label">Date</label>
          <input
              v-model="newProgress.date"
              type="date"
              class="form-control"
              id="date"
              required
          />
        </div>

        <div class="col-md-4">
          <label for="weight" class="form-label">Weight</label>
          <input
              v-model.number="newProgress.weight"
              type="number"
              class="form-control"
              id="weight"
              step="0.1"
              required
          />
        </div>

        <div class="col-md-4">
          <label for="notes" class="form-label">Notes</label>
          <input
              v-model="newProgress.notes"
              type="text"
              class="form-control"
              id="notes"
          />
        </div>
      </div>

      <button type="submit" class="btn btn-primary mt-3">Add Progress</button>
    </form>

    <div v-if="progressEntries.length > 0">
      <div class="list-group">
        <div
            v-for="entry in progressEntries"
            class="list-group-item"
        >
          <div class="d-flex justify-content-between">
            <div>
              <strong>Date:</strong> {{ formatDate(entry.date) }}<br/>
              <strong>Weight:</strong> {{ entry.weight }} kg<br/>
              <strong>Notes:</strong> {{ entry.notes }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-info">
      No progress entries found. Start tracking your progress!
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from "vue";
import {getProgress, postProgress, type ProgressEntry} from "@/composables/ProgressActions.ts";

const progressEntries = ref<ProgressEntry[]>([]);
const newProgress = ref<ProgressEntry>({
  date: '',
  weight: 0,
  notes: "",
});

const fetchProgressEntries = async () => {
  progressEntries.value = await getProgress()
};
onMounted(fetchProgressEntries);


const submitForm = async () => {
      try {
        await postProgress(newProgress.value);
        newProgress.value = {date: '', weight: 0, notes: ""};
        fetchProgressEntries();

      } catch
          (error) {
        console.error("Failed to add progress entry:", error);
        alert("Failed to add progress entry. Please try again.");
      }
    }
;

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};
</script>

<style scoped>
</style>