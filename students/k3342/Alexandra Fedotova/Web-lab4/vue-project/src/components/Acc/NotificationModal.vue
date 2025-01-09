<template>
  <div
    class="modal fade"
    id="editProfileModal"
    aria-labelledby="editProfileModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editProfileModalLabel">Edit Profile</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close modal window"
          ></button>
        </div>
        <div class="modal-body">
          <form id="editProfileForm">
            <div class="mb-3">
              <label for="userAge" class="form-label">Age</label>
              <input
                type="number"
                class="form-control"
                v-model="profile.age"
                id="userAge"
                required
              />
            </div>
            <div class="mb-3">
              <label for="userHeight" class="form-label">Height</label>
              <input
                type="number"
                step="0.1"
                class="form-control"
                v-model="profile.height"
                id="userHeight"
                required
              />
            </div>
            <div class="mb-3">
              <label for="userWeight" class="form-label">Weight</label>
              <input
                type="number"
                step="0.1"
                class="form-control"
                v-model="profile.weight"
                id="userWeight"
                required
              />
            </div>
            <div class="mb-3">
              <label for="fitnessLevelEdit" class="form-label">Fitness Level</label>
              <select
                class="form-control"
                v-model="profile.fitness_level"
                id="fitnessLevelEdit"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="userGoals" class="form-label">Goals</label>
              <select class="form-control" v-model="profile.goals" id="userGoals">
                <option>Lose weight</option>
                <option>Gain weight</option>
                <option>Improve endurance</option>
                <option>Build muscle</option>
                <option>Increase flexibility</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="userProgress" class="form-label">Progress</label>
              <input
                type="text"
                class="form-control"
                v-model="profile.progress"
                id="userProgress"
                required
              />
            </div>
            <div
              v-if="errorMessage"
              class="alert alert-danger mt-3"
              role="alert"
            >
              {{ errorMessage }}
            </div>
            <div
              v-if="successMessage"
              class="alert alert-success mt-3"
              role="alert"
            >
              {{ successMessage }}
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="handleSaveClick"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from "bootstrap";

export default {
  props: {
    userId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      profile: {
        age: null,
        height: null,
        weight: null,
        fitness_level: "beginner",
        goals: "Lose weight",
        progress: "",
      },
      errorMessage: "",
      successMessage: "",
    };
  },
  mounted() {
    this.loadProfile();
    this.initModal();
  },
  methods: {
    initModal() {
      const modalElement = document.getElementById("editProfileModal");
      const bootstrapModal = Modal.getOrCreateInstance(modalElement);

      modalElement.addEventListener("hidden.bs.modal", () => {
        this.errorMessage = "";
        this.successMessage = "";
      });
    },
    async loadProfile() {
      try {
        const response = await fetch("http://127.0.0.1:8000/app/profiles/");
        if (!response.ok) throw new Error(`Error ${response.status}`);
        const profiles = await response.json();
        const user = profiles.find((p) => p.user === this.userId);
        if (user) this.profile = { ...user };
      } catch (error) {
        console.error("Error loading profile:", error);
      }
    },
    async handleSaveClick() {
      console.log("Save Changes button clicked");

      const endpoint = this.profile.id
        ? `http://127.0.0.1:8000/app/profiles/${this.profile.id}/update/`
        : "http://127.0.0.1:8000/app/profiles/create/";
      const method = this.profile.id ? "PATCH" : "POST";

      // Преобразование значений в числа с плавающей точкой
      const requestData = {
        age: this.profile.age,
        height: this.profile.height ? parseFloat(this.profile.height).toFixed(2) : null,
        weight: this.profile.weight ? parseFloat(this.profile.weight).toFixed(2) : null,
        fitness_level: this.profile.fitness_level.toLowerCase(),
        goals: this.profile.goals,
        progress: this.profile.progress,
      };

      console.log("Sending data:", requestData);

      try {
        const response = await fetch(endpoint, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(requestData),
        });
        if (!response.ok) throw new Error(`Error ${response.status}`);
        this.successMessage = this.profile.id
          ? "Profile updated!"
          : "Profile created!";
        setTimeout(() => (this.successMessage = ""), 3000);
        this.closeModal();
      } catch (error) {
        this.errorMessage = "Failed to save changes.";
        console.error("Error saving profile:", error);
      }
    },
    closeModal() {
      const modalElement = document.getElementById("editProfileModal");
      const bootstrapModal = Modal.getOrCreateInstance(modalElement);

      bootstrapModal.hide();

      const backdrop = document.querySelector(".modal-backdrop");
      if (backdrop) {
      backdrop.remove();
  }
      document.body.style.overflow = "";
    },
  },
};
</script>

<style>
</style>
