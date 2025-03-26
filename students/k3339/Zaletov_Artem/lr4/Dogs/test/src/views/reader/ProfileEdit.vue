<template>
  <div class="edit">
    <h2 class="edit-title">Edit the Profile</h2>
    <v-form
      @submit.prevent="saveChanges"
      ref="changeForm"
      class="form-container">
      <v-row>
        <v-col cols="12" md="6" class="mx-auto">
          <v-text-field
            label="First name"
            v-model="changeForm.first_name"
            name="first_name"
            outlined
            dense
            class="input-field"/>

          <v-text-field
            label="Last name"
            v-model="changeForm.last_name"
            name="last_name"
            outlined
            dense
            class="input-field"/>

          <v-text-field
            label="Telephone number"
            v-model="changeForm.tel"
            name="tel"
            outlined
            dense
            class="input-field"/>

          <v-btn type="submit" class="save-button" color="primary" dark>Save</v-btn>
        </v-col>
      </v-row>
    </v-form>
    <p class="back-link">
      <router-link to="/show/profile" class="back-button">Back</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'ProfileEdit',

  data: () => ({
    reader_old: Object,
    changeForm: {
      first_name: '',
      last_name: '',
      tel: '',
    },
  }),

  methods: {
    async saveChanges () {
      for (const [key, value] of Object.entries(this.changeForm)) {
        if (value === '') {
          delete this.changeForm[key]
        }
      }
      try {
        const response = await this.axios
          .patch('http://127.0.0.1:8000/auth/users/me/',
            this.changeForm, {
              headers: {
                Authorization: `Token ${sessionStorage.getItem('auth_token')}`
              }
              })
        console.log(response)
        this.$refs.changeForm.reset()
        await this.$router.push({name: 'profile'})
      } catch (e) {
        console.error(e.message)
      }
    }
  }
}
</script>

<style scoped>
.edit {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
}

.edit-title {
  font-size: 2rem;
  color: #3f51b5;
  margin-bottom: 2rem;
}

.form-container {
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 2rem;
  background-color: #fff;
}

.input-field {
  margin-bottom: 1.5rem;
}

.save-button {
  width: 100%;
  padding: 10px;
  font-weight: bold;
  border-radius: 8px;
}

.back-link {
  margin-top: 1.5rem;
  text-align: center;
}

.back-button {
  text-decoration: none;
  color: #283593;
  font-weight: bold;
  transition: color 0.3s ease;
}

.back-button:hover {
  color: #1a237e;
}
</style>
