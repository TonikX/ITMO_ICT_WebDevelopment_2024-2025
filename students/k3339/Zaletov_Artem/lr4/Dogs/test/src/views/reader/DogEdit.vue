<template>
  <div class="edit-container">
    <v-card class="edit-card">
      <v-card-title>Edit Dog Information</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateDog" ref="editForm">
          <v-text-field label="Dog's Name" v-model="editForm.name" outlined dense />
          <v-text-field label="Breed" v-model="editForm.breed" outlined dense />
          <v-text-field label="Age" v-model="editForm.age" type="number" outlined dense />
          <v-text-field label="Pedigree" v-model="editForm.family" outlined dense />
          <v-text-field label="Owner Info" v-model="editForm.owner_data" outlined dense />

          <v-btn color="primary" block class="mt-3" @click="updateDog">
            <v-icon left>mdi-content-save</v-icon> Update Dog Info
          </v-btn>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="blue darken-2" class="back-link" @click="goParticipants">
          <v-icon left>mdi-arrow-left</v-icon> Back
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    dogId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      editForm: {
        name: '',
        breed: '',
        age: '',
        family: '',
        owner_data: ''
      }
    };
  },
  mounted() {
    console.log("Dog ID:", this.dogId);
    this.loadDogData();
  },
  methods: {

  goParticipants() {
    this.$router.push({ path: "/participants" });
  },


    async loadDogData() {
      try {
        const response = await this.axios.get(`http://127.0.0.1:8000/participants/${this.dogId}`);
        this.editForm = response.data;
      } catch (error) {
        console.error("Error loading dog data:", error);
      }
    },
    async updateDog() {
      try {
        const response = await this.axios.patch(`http://127.0.0.1:8000/participants/${this.dogId}/`, this.editForm, {
          headers: {
            Authorization: `Token ${sessionStorage.getItem('auth_token')}`
          }
        });
        console.log(response);
        this.$router.push({ path: "/participants" });
      } catch (e) {
        console.error(e.response ? e.response.data : e.message);
      }
    }
  }
};
</script>

<style scoped>
.edit-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.edit-card {
  width: 400px;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.back-link {
  text-transform: none;
  font-weight: bold;
}
</style>
