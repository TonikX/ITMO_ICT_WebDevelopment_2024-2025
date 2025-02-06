<script>
import { useAuthStore } from '@/stores/auth';
import { mapStores } from 'pinia';
import { api } from '@/utils/api';

export default {
    emits: ['clubCreated'],
    data() {
        return {
            dialog: false,
            loading: false,

            newClub: {
                name: '',
                city: null,
                country: null,
                contact_user: null,
            },
            errors: {},

            countries: [],
            cities: [],
            users: [],
        }
    },
    computed: {
        ...mapStores(useAuthStore),
        filteredCities() {
            if (!this.newClub.country) return this.cities;
            return this.cities.filter(c =>
                c.country.id === this.newClub.country.id
            )
        },
    },
    methods: {
        async fetchCountries() {
            try {
                const res = await api.get('/countries/')
                this.countries = res.data
            } catch (e) {
                throw e
            }
        },
        async fetchCities() {
            try {
                const res = await api.get('/cities/')
                this.cities = res.data
            } catch (e) {
                throw e
            }
        },
        async fetchUsers() {
            try {
                const res = await api.get('/auth/users/')
                this.users = res.data
            } catch (e) {
                throw e
            }
        },
        async createClub() {
            try {
                this.loading = true
                this.errors = {}
                await api.post("/clubs/", {
                    name: this.newClub.name,
                    country: (this.newClub.city && this.newClub.country) ? null : (this.newClub.country?.id || null),
                    city: this.newClub.city?.id || null,
                    contact_user: this.newClub.contact_user?.id || null
                })
                this.newClub = {}
                this.dialog = false
                this.$emit('clubCreated')
            } catch (e) {
                this.errors = e.response?.data
            } finally {
                this.loading = false
            }
        },
    },
    mounted() {
        this.fetchCities()
        this.fetchCountries()
        this.fetchUsers()
    },
    watch: {
        'newClub.country'(newVal) {
            if (newVal) this.newClub.city = null
        }
    },
}
</script>
<template>
    <v-dialog v-model="dialog" max-width="500">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn v-if="authStore.user?.is_staff" @click="dialog = true" prepend-icon="mdi-plus"
                v-bind="activatorProps" variant="tonal" color="blue" block>New Club</v-btn>
        </template>
        <v-card class="pa-4" :loading="loading">
            <v-card-title>Create new club</v-card-title>
            <v-card-text>
                <v-text-field v-model="newClub.name" label="Name" :error-messages="errors.name"></v-text-field>
                <v-autocomplete v-model="newClub.country" :items="countries" item-title="name" label="Country"
                    return-object clearable :error-messages="errors.country"></v-autocomplete>
                <v-autocomplete v-model="newClub.city" :items="filteredCities" item-title="name" label="City"
                    return-object clearable :error-messages="errors.city"></v-autocomplete>
                <v-autocomplete v-model="newClub.contact_user" :items="users"
                    :item-title="user => `${user.first_name} ${user.last_name} (@${user.username})`"
                    label="Contact user" return-object clearable :error-messages="errors.contact_user"></v-autocomplete>
                <p v-if="errors.non_field_errors?.length" class="mt-2 text-red-darken-2">
                    {{ errors.non_field_errors.join(' ') }}
                </p>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn variant="tonal" @click="dialog = false">Cancel</v-btn>
                <v-btn variant="tonal" @click="createClub">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>