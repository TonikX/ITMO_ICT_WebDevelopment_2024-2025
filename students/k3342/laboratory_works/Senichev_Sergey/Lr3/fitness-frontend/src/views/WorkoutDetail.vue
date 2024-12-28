<template>
    <v-container v-if="workout">
      <v-card>
        <v-card-title class="headline">{{ workout.title }}</v-card-title>
        <v-card-text>
          <v-row>
            <!-- Workout Info -->
            <v-col cols="12" md="8">
              <v-card outlined>
                <v-card-text>
                  <h3>Description</h3>
                  <p>{{ workout.description }}</p>
                  <v-divider class="my-4"></v-divider>
                  <h3>Details</h3>
                  <v-list dense>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Type: {{ workout.type }}</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Duration: {{ workout.duration }}</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Difficulty: {{ workout.difficulty }}/5</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                  <v-divider class="my-4"></v-divider>
                  <h3>Equipment Needed</h3>
                  <v-chip-group>
                    <v-chip v-for="(eq, index) in workout.equipment" :key="index">
                      {{ eq }}
                    </v-chip>
                  </v-chip-group>
                </v-card-text>
              </v-card>
            </v-col>
  
            <!-- Trainer Info -->
            <v-col cols="12" md="4">
              <v-card outlined>
                <v-card-title>Trainer</v-card-title>
                <v-card-text>
                  <v-avatar size="120" class="mb-4">
                    <v-img :src="workout.trainer.image_url"></v-img>
                  </v-avatar>
                  <h3>{{ workout.trainer.name }}</h3>
                  <p>{{ workout.trainer.title }}</p>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
  
        <v-card-actions>
          <v-btn
            color="primary"
            @click="startWorkout"
            :loading="loading"
            :disabled="loading"
          >
            Start Workout
          </v-btn>
          <v-btn
            color="success"
            @click="completeWorkout"
            :loading="loading"
            :disabled="loading || !workoutStarted"
          >
            Complete Workout
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn icon @click="toggleSaved">
            <v-icon>{{ isSaved ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </template>
  
  <script>
  import { mapState } from 'vuex'
  import axios from 'axios'
  
  export default {
    name: 'WorkoutDetail',
    data: () => ({
      workout: null,
      loading: false,
      workoutStarted: false
    }),
    computed: {
      ...mapState(['savedWorkouts']),
      isSaved() {
        return this.savedWorkouts.some(saved => saved.id === this.workout.id)
      }
    },
    methods: {
      async fetchWorkout() {
        try {
          const response = await axios.get(`workouts/${this.$route.params.id}/`)
          this.workout = response.data
        } catch (error) {
          console.error('Error fetching workout:', error)
        }
      },
      async startWorkout() {
        this.loading = true
        try {
          await axios.post(`workouts/${this.workout.id}/start/`)
          this.workoutStarted = true
          this.$store.commit('SET_SNACKBAR', {
            text: 'Workout started!',
            color: 'success'
          })
        } catch (error) {
          console.error('Error starting workout:', error)
        } finally {
          this.loading = false
        }
      },
      async completeWorkout() {
        this.loading = true
        try {
          await axios.post(`workouts/${this.workout.id}/complete/`)
          this.workoutStarted = false
          this.$store.commit('SET_SNACKBAR', {
            text: 'Workout completed!',
            color: 'success'
          })
        } catch (error) {
          console.error('Error completing workout:', error)
        } finally {
          this.loading = false
        }
      },
      async toggleSaved() {
        try {
          if (this.isSaved) {
            await this.$store.dispatch('removeSavedWorkout', this.workout.id)
          } else {
            await this.$store.dispatch('addSavedWorkout', this.workout.id)
          }
        } catch (error) {
          console.error('Error toggling saved workout:', error)
        }
      }
    },
    async created() {
      await this.fetchWorkout()
    }
  }
  </script>