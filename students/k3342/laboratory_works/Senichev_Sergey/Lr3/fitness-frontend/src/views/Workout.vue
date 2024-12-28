<template>
  <v-container>
    <v-row>
      <!-- Filters -->
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title>Filters</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="4">
                <v-select
                  v-model="filters.type"
                  :items="workoutTypes"
                  label="Workout Type"
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="12" sm="4">
                <v-select
                  v-model="filters.difficulty"
                  :items="[1,2,3,4,5]"
                  label="Difficulty"
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="search"
                  label="Search"
                  prepend-icon="mdi-magnify"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Workout Cards -->
      <v-col v-for="workout in filteredWorkouts" :key="workout.id" cols="12" sm="6" md="4">
        <v-card class="mb-4">
          <v-card-title>{{ workout.title }}</v-card-title>
          <v-card-text>
            <div>Type: {{ workout.type }}</div>
            <div>Duration: {{ workout.duration }}</div>
            <div>Difficulty: {{ workout.difficulty }}/5</div>
            <v-chip-group>
              <v-chip v-for="(eq, index) in workout.equipment" :key="index">
                {{ eq }}
              </v-chip>
            </v-chip-group>
          </v-card-text>
          <v-card-actions>
            <v-btn
              text
              color="primary"
              :to="{ name: 'WorkoutDetail', params: { id: workout.id }}"
            >
              View Details
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn icon @click="toggleSaved(workout)">
              <v-icon>{{ isSaved(workout) ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Workouts',
  data: () => ({
    search: '',
    filters: {
      type: null,
      difficulty: null
    },
    workoutTypes: ['Cardio', 'Strength', 'Flexibility']
  }),
  computed: {
    ...mapState(['workouts', 'savedWorkouts']),
    filteredWorkouts() {
      return this.workouts.filter(workout => {
        if (this.filters.type && workout.type !== this.filters.type) return false
        if (this.filters.difficulty && workout.difficulty !== this.filters.difficulty) return false
        if (this.search) {
          const searchLower = this.search.toLowerCase()
          return workout.title.toLowerCase().includes(searchLower) ||
                 workout.description.toLowerCase().includes(searchLower)
        }
        return true
      })
    }
  },
  methods: {
    ...mapActions(['fetchWorkouts']),
    isSaved(workout) {
      return this.savedWorkouts.some(saved => saved.id === workout.id)
    },
    async toggleSaved(workout) {
      try {
        if (this.isSaved(workout)) {
          await this.$store.dispatch('removeSavedWorkout', workout.id)
        } else {
          await this.$store.dispatch('addSavedWorkout', workout.id)
        }
      } catch (error) {
        console.error('Error toggling saved workout:', error)
      }
    }
  },
  async created() {
    try {
      await this.fetchWorkouts()
    } catch (error) {
      console.error('Error fetching workouts:', error)
    }
  }
}
</script>