<template>
  <v-container fluid class="fill-height bg-gradient">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="5" xl="4">
        <v-card class="auth-card elevation-8" rounded="lg">
          <div class="auth-header text-center py-6">
            <v-icon size="64" color="primary" class="mb-2">mdi-account-plus</v-icon>
            <h1 class="text-h4 font-weight-bold mt-2">Create Account</h1>
            <p class="text-grey mt-2">Join Publishing System</p>
          </div>
          
          <v-card-text class="px-6">
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="username"
                label="Username"
                autocomplete="username"
                prepend-inner-icon="mdi-account-outline"
                variant="underlined"
                :error-messages="errors.username"
                required
                autofocus
                class="mb-6"
              />
              <v-text-field
                v-model="email"
                label="Email"
                autocomplete="email"
                prepend-inner-icon="mdi-email-outline"
                type="email"
                variant="underlined"
                :error-messages="errors.email"
                required
                class="mb-6"
              />
              <v-text-field
                v-model="password"
                label="Password"
                autocomplete="new-password"
                prepend-inner-icon="mdi-lock-outline"
                type="password"
                variant="underlined"
                :error-messages="errors.password"
                required
                class="mb-6"
              />
              <v-text-field
                v-model="passwordRetype"
                label="Confirm Password"
                autocomplete="new-password"
                prepend-inner-icon="mdi-lock-check-outline"
                type="password"
                variant="underlined"
                :error-messages="errors.passwordRetype"
                required
                class="mb-2"
              />
              
              <v-alert
                v-if="authStore.error"
                type="error"
                variant="tonal"
                class="mb-4"
                closable
                @click:close="authStore.error = null"
                rounded="lg"
              >
                {{ authStore.error }}
              </v-alert>
              
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                class="font-weight-bold my-4"
                :loading="authStore.loading"
              >
                Create Account
              </v-btn>
            </v-form>
          </v-card-text>
          
          <v-divider class="my-4" />
          
          <v-card-text class="text-center pb-6">
            <span class="text-grey">Already have an account? </span>
            <v-btn variant="text" to="/login" color="primary" class="font-weight-bold">
              Sign in
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const passwordRetype = ref('')
const errors = reactive<{
  username: string[]
  email: string[]
  password: string[]
  passwordRetype: string[]
}>({
  username: [],
  email: [],
  password: [],
  passwordRetype: [],
})

async function handleRegister() {
  errors.username = []
  errors.email = []
  errors.password = []
  errors.passwordRetype = []

  if (!username.value) {
    errors.username.push('Username is required')
  }
  if (!email.value) {
    errors.email.push('Email is required')
  }
  if (!password.value) {
    errors.password.push('Password is required')
  }
  if (!passwordRetype.value) {
    errors.passwordRetype.push('Password confirmation is required')
  }
  if (password.value && passwordRetype.value && password.value !== passwordRetype.value) {
    errors.passwordRetype.push('Passwords do not match')
  }

  if (errors.username.length || errors.email.length || errors.password.length || errors.passwordRetype.length) {
    return
  }

  const result = await authStore.register(username.value, email.value, password.value)

  if (result.success) {
    router.push('/')
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.bg-gradient {
  background: linear-gradient(135deg, #EC4899 0%, #F97316 25%, #7C3AED 75%, #06B6D4 100%);
  position: relative;
}

.auth-card {
  background: white;
  border-radius: 16px;
}

.auth-header {
  background: linear-gradient(135deg, #EC4899 0%, #F97316 100%);
  color: white;
  border-radius: 16px 16px 0 0;
  margin: -16px -16px 0 -16px;
}

.auth-header h1, .auth-header p {
  color: white;
}

:deep(.v-field__underline::before) {
  border-color: rgba(236, 72, 153, 0.3);
}

:deep(.v-field--focused .v-field__underline::before) {
  border-color: #EC4899;
}
</style>

