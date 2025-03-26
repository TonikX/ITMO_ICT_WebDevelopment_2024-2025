<template>
  <div class="participants-container">
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          v-model="selectedBreed"
          :items="breedOptions"
          label="Фильтр по породе"
          clearable
          class="custom-select"
        ></v-select>
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          v-model="selectedClub"
          :items="clubOptions"
          label="Фильтр по клубу"
          clearable
          class="custom-select"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="participant in filteredParticipants" :key="participant.id" cols="12" md="6" lg="4">
        <v-card elevation="5" class="participant-card">
          <v-card-title class="card-title">{{ participant.name }}</v-card-title>
          <v-card-text>
            <div class="info-item"><strong>Порода:</strong> {{ participant.breed }}</div>
            <div class="info-item"><strong>Возраст:</strong> {{ participant.age }}</div>
            <div class="info-item"><strong>Родословная:</strong> {{ participant.family }}</div>
            <div class="info-item"><strong>Информация о владельце:</strong> {{ participant.owner_data }}</div>
            <div class="info-item"><strong>Клуб:</strong> {{ participant.club }}</div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" class="edit-btn" @click="editParticipant(participant.id)">Редактировать</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  props: {
    participants: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      selectedBreed: null,
      selectedClub: null
    };
  },
  computed: {
    breedOptions() {
      return [...new Set(this.participants.map(p => p.breed))];
    },
    clubOptions() {
      return [...new Set(this.participants.map(p => p.club))];
    },
    filteredParticipants() {
      return this.participants.filter(p => {
        const matchesBreed = this.selectedBreed ? p.breed === this.selectedBreed : true;
        const matchesClub = this.selectedClub ? p.club === this.selectedClub : true;
        return matchesBreed && matchesClub;
      });
    }
  },
  methods: {
    editParticipant(participantId) {
      this.$router.push({ name: 'Dog_edit', params: { dogId: participantId } });
    }
  }
};
</script>

<style scoped>
.participants-container {
  padding: 24px;
  background: #f0f4ff;
  border-radius: 12px;
}

.custom-select {
  max-width: 400px;
  margin: 0 auto 16px;
}

.participant-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease-in-out;
}

.participant-card:hover {
  transform: translateY(-5px);
}

.card-title {
  font-size: 20px;
  font-weight: bold;
  color: #1e3a8a;
  text-align: center;
  margin-bottom: 12px;
}

.info-item {
  font-size: 16px;
  margin-bottom: 8px;
  padding: 8px 12px;
