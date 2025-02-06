<script>
import { mapStores } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import { api } from '@/utils/api';
export default {
    data() {
        return {
            isEditing: false,
            hasSaved: false,

            userDraft: {},
            errors: {},
            cities: [],

        }
    },
    computed: {
        ...mapStores(useAuthStore)
    },
    watch: {
        'authStore.user': {
            handler(newUser) {
                if (newUser) {
                    this.userDraft = { ...newUser }
                }
            },
            immediate: true
        }
    },
    methods: {
        async save() {
            this.errors = {}
            try {
                const res = await api.patch('/auth/users/me/', { ...this.userDraft })
                this.authStore.user = res.data

                this.hasSaved = true
                this.isEditing = false
            } catch (err) {
                this.errors = err.response?.data
            }
        },
        cancel() {
            this.userDraft = { ...this.authStore.user };
            this.isEditing = false;
            this.errors = {}
        },
        async fetchCities() {
            try {
                const res = await api.get('/cities/')
                this.cities = res.data
            } catch (e) {
                this.cities = []
                throw (e)
            }
        },
    },
    mounted() {
        this.fetchCities()
    }

}
</script>

<template>
    <v-sheet class="d-flex flex-column ga-6 mx-auto" max-width="500">
        <h1>Profile</h1>
        <v-card v-if="authStore.user?.club" color="blue-lighten-5" max-width="500">
            <v-card-title>Club</v-card-title>
            <v-card-text>
                {{ authStore.user.club.name }}
            </v-card-text>
        </v-card>
        <v-card max-width="500">
            <v-card-title>User info</v-card-title>
            <v-card-text>
                <v-text-field v-model="userDraft.username" :readonly="!isEditing" label="Username"
                    :error-messages="errors.username"></v-text-field>
                <v-text-field v-model="userDraft.email" :readonly="!isEditing" label="Email"
                    :error-messages="errors.email"></v-text-field>
                <v-text-field v-model="userDraft.first_name" :readonly="!isEditing" label="First Name"
                    :error-messages="errors.first_name"></v-text-field>
                <v-text-field v-model="userDraft.last_name" :readonly="!isEditing" label="Last Name"
                    :error-messages="errors.last_name"></v-text-field>
                <v-text-field v-model="userDraft.phone_number" :readonly="!isEditing" label="Phone Number"
                    :error-messages="errors.phone_number"></v-text-field>
                <v-autocomplete v-model="userDraft.city" :readonly="!isEditing" label="City" :items="cities"
                    item-title="name" item-value="id"></v-autocomplete>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn variant="tonal" @click="isEditing ? cancel() : (isEditing = true)" width="80">
                    <v-fade-transition leave-absolute>
                        <span v-if="isEditing">Cancel</span>
                        <span v-else>Edit</span>
                    </v-fade-transition>
                </v-btn>
                <v-btn color="green" variant="tonal" :disabled="!isEditing" @click="save">Save</v-btn>
            </v-card-actions>

            <v-snackbar v-model="hasSaved" :timeout="2000" location="bottom left">
                Your profile has been updated
            </v-snackbar>
        </v-card>
    </v-sheet>


</template>