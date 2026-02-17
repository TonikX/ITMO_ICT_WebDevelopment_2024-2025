<template>
  <v-container class="py-8">
    <v-row class="mb-8">
      <v-col cols="12">
        <h1 class="text-h3 font-weight-bold">User Profile</h1>
        <p class="text-grey mt-2">Manage your account settings and security</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <v-card class="elevation-2" rounded="lg">
          <v-tabs v-model="tab" class="custom-tabs">
            <v-tab value="profile" prepend-icon="mdi-account-circle">Account Details</v-tab>
            <v-tab value="password" prepend-icon="mdi-lock-reset">Change Password</v-tab>
          </v-tabs>

          <v-divider />

          <v-window v-model="tab" class="pa-6">
            <!-- Profile Tab -->
            <v-window-item value="profile">
              <div class="mb-4">
                <h2 class="text-h6 font-weight-bold mb-4">Personal Information</h2>
              </div>

              <v-form @submit.prevent="handleUpdateProfile">
                <v-text-field
                  v-model="profileForm.username"
                  label="Username"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  :error-messages="profileErrors.username"
                  class="mb-4"
                  readonly
                />
                <v-text-field
                  v-model="profileForm.email"
                  label="Email Address"
                  prepend-inner-icon="mdi-email-outline"
                  variant="outlined"
                  type="email"
                  :error-messages="profileErrors.email"
                  class="mb-6"
                />

                <v-alert
                  v-if="profileError"
                  type="error"
                  variant="tonal"
                  class="mb-4"
                  closable
                  @click:close="profileError = null"
                  rounded="lg"
                >
                  {{ profileError }}
                </v-alert>

                <v-alert
                  v-if="profileSuccess"
                  type="success"
                  variant="tonal"
                  class="mb-4"
                  closable
                  @click:close="profileSuccess = false"
                  rounded="lg"
                >
                  ✓ Profile updated successfully!
                </v-alert>

                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  :loading="authStore.loading"
                  class="font-weight-bold"
                >
                  Save Changes
                </v-btn>
              </v-form>
            </v-window-item>

            <!-- Password Tab -->
            <v-window-item value="password">
              <div class="mb-4">
                <h2 class="text-h6 font-weight-bold mb-4">Update Your Password</h2>
                <p class="text-grey text-body-2">For your security, please use a strong password</p>
              </div>

              <v-form @submit.prevent="handleChangePassword">
                <v-text-field
                  v-model="passwordForm.current_password"
                  label="Current Password"
                  prepend-inner-icon="mdi-lock-outline"
                  type="password"
                  variant="outlined"
                  :error-messages="passwordErrors.current_password"
                  class="mb-4"
                />
                <v-text-field
                  v-model="passwordForm.new_password"
                  label="New Password"
                  prepend-inner-icon="mdi-lock-plus-outline"
                  type="password"
                  variant="outlined"
                  :error-messages="passwordErrors.new_password"
                  class="mb-4"
                />
                <v-text-field
                  v-model="passwordForm.re_new_password"
                  label="Confirm New Password"
                  prepend-inner-icon="mdi-lock-check-outline"
                  type="password"
                  variant="outlined"
                  :error-messages="passwordErrors.re_new_password"
                  class="mb-6"
                />

                <v-alert
                  v-if="passwordError"
                  type="error"
                  variant="tonal"
                  class="mb-4"
                  closable
                  @click:close="passwordError = null"
                  rounded="lg"
                >
                  {{ passwordError }}
                </v-alert>

                <v-alert
                  v-if="passwordSuccess"
                  type="success"
                  variant="tonal"
                  class="mb-4"
                  closable
                  @click:close="passwordSuccess = false"
                  rounded="lg"
                >
                  ✓ Password changed successfully!
                </v-alert>

                <v-btn
                  type="submit"
                  color="secondary"
                  size="large"
                  :loading="authStore.loading"
                  class="font-weight-bold"
                >
                  Update Password
                </v-btn>
              </v-form>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="elevation-2" rounded="lg" style="background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%); color: white;">
          <v-card-text class="text-center pa-6">
            <v-icon size="64" class="mb-4 d-block">mdi-shield-account</v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">Account Security</h3>
            <p class="text-body-2 opacity-75 mb-4">Keep your account safe with a strong password</p>
            <v-divider class="my-4" style="opacity: 0.3;" />
            <p class="text-body-2 font-weight-bold">Current User</p>
            <p class="text-h6 font-weight-bold">{{ authStore.user?.username }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const tab = ref('profile')

const profileForm = reactive({
  username: '',
  email: '',
})

const profileErrors = reactive<{
  username: string[]
  email: string[]
}>({
  username: [],
  email: [],
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  re_new_password: '',
})

const passwordErrors = reactive<{
  current_password: string[]
  new_password: string[]
  re_new_password: string[]
}>({
  current_password: [],
  new_password: [],
  re_new_password: [],
})

const profileError = ref<string | null>(null)
const profileSuccess = ref(false)
const passwordError = ref<string | null>(null)
const passwordSuccess = ref(false)

onMounted(() => {
  if (authStore.user) {
    profileForm.username = authStore.user.username || ''
    profileForm.email = authStore.user.email || ''
  }
})

async function handleUpdateProfile() {
  Object.keys(profileErrors).forEach(key => {
    profileErrors[key as keyof typeof profileErrors] = []
  })
  profileError.value = null
  profileSuccess.value = false

  const result = await authStore.updateProfile({
    username: profileForm.username || undefined,
    email: profileForm.email || undefined,
  })

  if (result.success) {
    profileSuccess.value = true
    setTimeout(() => {
      profileSuccess.value = false
    }, 3000)
  } else {
    profileError.value = result.error || 'Error updating profile'
  }
}

async function handleChangePassword() {
  Object.keys(passwordErrors).forEach(key => {
    passwordErrors[key as keyof typeof passwordErrors] = []
  })
  passwordError.value = null
  passwordSuccess.value = false

  if (!passwordForm.current_password) {
    passwordErrors.current_password.push('Current password is required')
  }
  if (!passwordForm.new_password) {
    passwordErrors.new_password.push('New password is required')
  }
  if (!passwordForm.re_new_password) {
    passwordErrors.re_new_password.push('Password confirmation is required')
  }
  if (passwordForm.new_password && passwordForm.re_new_password &&
      passwordForm.new_password !== passwordForm.re_new_password) {
    passwordErrors.re_new_password.push('Passwords do not match')
  }

  if (passwordErrors.current_password.length ||
      passwordErrors.new_password.length ||
      passwordErrors.re_new_password.length) {
    return
  }

  const result = await authStore.changePassword(
    passwordForm.current_password,
    passwordForm.new_password,
    passwordForm.re_new_password
  )

  if (result.success) {
    passwordSuccess.value = true
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.re_new_password = ''
    setTimeout(() => {
      passwordSuccess.value = false
    }, 3000)
  } else {
    passwordError.value = result.error || 'Error changing password'
  }
}
</script>

<style scoped>
:deep(.custom-tabs) {
  background: rgba(124, 58, 237, 0.05);
}

:deep(.custom-tabs .v-tab) {
  text-transform: none;
  letter-spacing: 0;
  font-weight: 500;
}

:deep(.custom-tabs .v-tab--selected) {
  color: #7C3AED;
}

:deep(.custom-tabs .v-tab--selected::after) {
  background: #7C3AED;
}
</style>

