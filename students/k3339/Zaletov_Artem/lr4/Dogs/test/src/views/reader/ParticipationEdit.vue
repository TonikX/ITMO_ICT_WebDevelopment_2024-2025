<template>
  <div class="edit">
    <h3>Edit Grade</h3>
    <v-form @submit.prevent="updatePart" ref="editFormPart" class="my-2">
      <v-row>
        <v-col cols="5" class="mx-auto">
          <v-select
            v-model="editFormPart.participant"
            :items="participants"
            item-text="name"
            item-value="id"
            name="participant"
            label="Participant"
            disabled
          ></v-select>

          <v-select
            v-model="editFormPart.medal"
            :items="medals"
            name="medal"
            label="Medal"
          ></v-select>

          <v-text-field
            label="Date of vaccination"
            v-model="editFormPart.vaccinated"
            name="vaccinated"
            type="date"
          />

          <v-checkbox v-model="editFormPart.dismissed" :label="'Dismissed'" />

          <v-text-field
            label="Enter the grade"
            v-model="editFormPart.final_grade"
            type="number"
            name="final_grade"
          />

          <v-btn type="submit" color="#283593" dark>Update</v-btn>
        </v-col>
      </v-row>
    </v-form>
    <v-card>
      <v-card-text style="margin-top:1cm">
        <a @click.prevent="goProfile" style="text-decoration: none; color: #283593">Back</a>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditDogGrade",
  props: ["dogId"],
  data: () => ({
    editFormPart: {
      id: null,
      medal: "",
      vaccinated: "",
      dismissed: false,
      final_grade: "",
      participant: "",
    },
    medals: ["g", "s", "b"],
    participants: [],
  }),
  methods: {
    async fetchParticipantData() {
      try {
        console.log("Fetching data for dogId:", this.dogId);
        const response = await axios.get(`http://127.0.0.1:8000/participation/${this.dogId}/`);
        this.editFormPart = response.data;
        this.editFormPart.id = this.dogId;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async updatePart() {
      if (!this.editFormPart.id) {
        console.error("Error: ID is missing!");
        return;
      }
      try {
        await axios.patch(`http://127.0.0.1:8000/participation/${this.editFormPart.id}/`, this.editFormPart);
        alert("Updated successfully");
      } catch (error) {
        console.error("Error updating data:", error);
      }
    },
    goProfile() {
      this.$router.push({ name: "profile" });
    },
  },
  async mounted() {
    if (this.dogId) {
      await this.fetchParticipantData();
    } else {
      console.error("Error: dogId is missing from route params");
    }
  }
};
</script>