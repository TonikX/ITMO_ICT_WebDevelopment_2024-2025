<script>
import { api } from '@/utils/api';
import { mapStores } from 'pinia';
import { useAuthStore } from '@/stores/auth';


export default {
    data() {
        return {
            username: '',
            password: '',
            first_name: '',
            last_name: '',
            email: '',
            phone_number: '',
            city: '',

            cities: [],

            loading: false,
            errors: {
                username: [],
                password: [],
                first_name: [],
                last_name: [],
                email: [],
                non_field_errors: []
            },
            rules: {
                required: value => !!value || 'Required.',
                email: value => {
                    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                    return pattern.test(value) || 'Invalid e-mail.'
                },
                phone: value => {
                    if (!value) return true;
                    const pattern = /^(\+?[0-9]{1,3})?[-.\s]?(\(?\d{3}\)?)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}$/;
                    return pattern.test(value) || 'Invalid phone number.';
                },

            }
        }
    },
    computed: {
        ...mapStores(useAuthStore)
    },
    methods: {
        async fetchCities() {
            try {
                const res = await api.get('/cities/')
                this.cities = res.data
            } catch (e) {
                this.cities = []
                throw (e)
            }
        },
        async handleRegister() {
            const { valid } = await this.$refs.form.validate()
            if (!valid) return
            const formData = {
                username: this.username,
                password: this.password,
                first_name: this.first_name,
                last_name: this.last_name,
                email: this.email,
                phone_number: this.phone_number,
                city: this.city,
            };
            try {
                this.loading = true
                this.errors = {
                    username: [],
                    password: [],
                    first_name: [],
                    last_name: [],
                    email: [],
                    non_field_errors: []
                }
                const res = await api.post('/auth/users/', formData)
                await this.authStore.login({
                    username: this.username,
                    password: this.password
                });
                this.$router.push('/');
            } catch (error) {
                if (error.response && error.response.data) {
                    this.errors = { ...this.errors, ...error.response.data };
                } else {
                    this.errors.non_field_errors = ['Something went wrong :('];
                }
            } finally {
                this.loading = false
            }
        }
    },
    mounted() {
        this.fetchCities()
    }
} 
</script>

<template>
    <v-card class="mx-auto d-flex flex-column pa-8" max-width="400">
        <h2 class="mb-4">Register</h2>
        <v-form @submit.prevent="handleRegister" ref="form">
            <v-text-field v-model="username" label="Username*" prepend-inner-icon="mdi-account"
                :error-messages="errors.username" :rules="[rules.required]" density="compact"></v-text-field>
            <v-text-field v-model="password" type="password" label="Password*" prepend-inner-icon="mdi-lock"
                :error-messages="errors.password" :rules="[rules.required]" density="compact"></v-text-field>
            <v-text-field v-model="first_name" label="First Name*" :error-messages="errors.first_name"
                :rules="[rules.required]" density="compact"></v-text-field>
            <v-text-field v-model="last_name" label="Last Name*" :error-messages="errors.last_name"
                :rules="[rules.required]" density="compact"></v-text-field>
            <v-text-field v-model="email" label="Email*" prepend-inner-icon="mdi-at" :error-messages="errors.email"
                :rules="[rules.required, rules.email]" density="compact"></v-text-field>
            <v-text-field v-model="phone_number" label="Phone" prepend-inner-icon="mdi-phone"
                :error-messages="errors.phone_number" :rules="[rules.phone]" density="compact"></v-text-field>
            <v-autocomplete v-model="city" label="City" :items="cities" item-title="name" item-value="id"
                prepend-inner-icon="mdi-city" density="compact"></v-autocomplete>

            <v-btn :loading='loading' type='submit' variant='tonal' block>Register</v-btn>
            <p v-if="errors.non_field_errors.length" class="mt-2 text-red-darken-2">
                {{ errors.non_field_errors.join(' ') }}
            </p>
        </v-form>
    </v-card>
</template>