<script>
import { mapStores } from 'pinia'
import { useAuthStore } from '@/stores/auth'

export default {
    data() {
        return {
            username: '',
            password: '',

            loading: false,
            errors: {
                username: [],
                password: [],
                non_field_errors: []
            }
        }
    },
    computed: {
        ...mapStores(useAuthStore)
    },
    methods: {
        async handleLogin() {
            try {
                this.loading = true
                this.errors = { username: [], password: [], non_field_errors: [] }
                await this.authStore.login({
                    username: this.username,
                    password: this.password
                })
                this.$router.push('/');
            } catch (error) {
                if (error.response && error.response.data) {
                    this.errors = { ...this.errors, ...error.response.data }
                } else {
                    this.errors.non_field_errors = ['Something went wrong :(']
                }
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<template>
    <v-card class="mx-auto d-flex flex-column pa-8" max-width="350">
        <h2 class="mb-4">Log in</h2>
        <v-form @submit.prevent="handleLogin" class="d-flex flex-column ga-3">
            <v-text-field v-model="username" label="Username" prepend-inner-icon="mdi-account"
                :error-messages="errors.username"></v-text-field>
            <v-text-field v-model="password" type="password" label="Password" prepend-inner-icon="mdi-lock"
                :error-messages="errors.password"></v-text-field>
            <v-btn :loading="loading" variant="tonal" type="submit" text="Login" block></v-btn>
            <p v-if="errors.non_field_errors.length" class="mt-2 text-red-darken-2">
                {{ errors.non_field_errors.join(' ') }}
            </p>
        </v-form>
    </v-card>
</template>