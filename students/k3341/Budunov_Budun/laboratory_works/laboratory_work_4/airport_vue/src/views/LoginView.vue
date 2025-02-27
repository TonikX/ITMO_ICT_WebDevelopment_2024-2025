<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card class="pa-10" max-width="500">
      <v-card-title class="text-h5 text-center">Airport management system</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submit" ref="form" class="form-container">
          <v-text-field
            v-model="username"
            label="Username"
            required
            outlined
            class="input-field mb-6"
            :rules="usernameRules"
          ></v-text-field>

          <v-text-field
            v-model="password"
            type="password"
            label="Password"
            required
            outlined
            class="input-field mb-8"
            :rules="passwordRules"
          ></v-text-field>

          <v-alert v-if="error" type="error" class="mb-4" prominent dismissible>
            {{ error }}
          </v-alert>

          <v-btn
            type="submit"
            color="primary"
            block
            class="mt-6"
            :loading="loading"
            :disabled="loading"
            @click="submit"
          >
            Login
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginView',
  data () {
    return {
      username: '',
      password: '',
      showPassword: false,
      error: null,
      loading: false,
      usernameRules: [
        (v) => !!v || 'Username is required'
      ],
      passwordRules: [
        (v) => !!v || 'Password is required'
      ]
    }
  },
  methods: {
    async submit () {
      this.error = null
      this.loading = true

      if (this.$refs.form.validate()) {
        try {
          const response = await axios.post('api/auth/jwt/create/', {
            username: this.username,
            password: this.password
          })
          const { access, refresh } = response.data

          const tokens = {
            access: access,
            refresh: refresh
          }
          localStorage.setItem('tokens', JSON.stringify(tokens))
          localStorage.setItem('isLoggedIn', true)

          const userResponse = await axios.get('api/auth/users/me/', {
            headers: {
              Authorization: `Bearer ${access}`
            }
          })
          localStorage.setItem('isAdmin', userResponse.data.is_admin)

          this.$router.push('/home')
        } catch (err) {
          if (err.response) {
            if (err.response.status === 400) {
              this.error = 'Invalid credentials.'
            } else {
              this.error = 'An error occurred during login.'
            }
          } else {
            this.error = 'Network error. Please try again.'
          }
        } finally {
          this.loading = false
        }
      } else {
        this.loading = false
      }
    }
  },
  mounted () {
    if (localStorage.getItem('isLoggedIn')) {
      this.$router.push('/home')
    }
  }
}
</script>

<style scoped>
.v-card {
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.v-card-title {
  font-weight: 500;
  margin-bottom: 30px;
  width: 100%;
}

.form-container {
  width: 100%;
}

.input-field {
  width: 100%;
  height: 56px;
}

.mb-6 {
  margin-bottom: 24px !important;
}

.mb-8 {
  margin-bottom: 32px !important;
}
</style>
