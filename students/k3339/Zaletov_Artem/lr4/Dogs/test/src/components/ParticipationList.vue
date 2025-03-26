<template>
  <div class="participation-container">
    <h2 class="title">Participation Details</h2>
    <div class="card-grid">
      <v-card v-for="participation in participations" :key="participation.id" elevation="3" class="small-card">
        <v-card-text>
          <p><strong>Medal:</strong> {{ participation.medal }}</p>
          <p><strong>Vaccine:</strong> {{ participation.vaccinated }}</p>
          <p><strong>Verified:</strong> {{ participation.dismissed }}</p>
          <p><strong>Grade:</strong> {{ participation.final_grade }}</p>
          <p><strong>Participant:</strong> {{ participation.participant}}</p>
          <v-btn color="primary" class="edit-button" @click="goParticipationsEdit(participation.id)">Edit</v-btn>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    participations: {
      type: Array,
      required: true
    }
  },
  methods:
      {
        goParticipationsEdit(dogId) {
        this.$router.push({ name: "Participation_Edit", params: { dogId: dogId } });
}


  }
}
</script>

<style scoped>
.participation-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #3f51b5;
  margin-bottom: 1rem;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  width: 100%;
  max-width: 800px;
}

.small-card {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 1rem;
  background-color: #ffffff;
  text-align: center;
  position: relative;
}

p {
  font-size: 0.9rem;
  margin: 5px 0;
}

.edit-button {
  margin-top: 10px;
  width: 100%;
}
</style>
