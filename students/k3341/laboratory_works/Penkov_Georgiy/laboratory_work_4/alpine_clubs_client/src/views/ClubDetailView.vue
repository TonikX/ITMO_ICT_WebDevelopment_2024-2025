<script>
import { api } from '@/utils/api';
import { useAuthStore } from '@/stores/auth';
import { mapStores } from 'pinia';
import ClubMembersTable from '@/components/ClubMembersTable.vue';


export default {
    components: { ClubMembersTable },
    props: {
        id: String,
    },
    data() {
        return {
            club: {},
            loading: false,

            editing: false,
            hasSaved: false,
            clubDraft: {},
            errors: {},

            countries: [],
            cities: [],
            users: [],

            isMember: false,
            membershipErrors: {}
        }
    },
    computed: {
        ...mapStores(useAuthStore),
        filteredCities() {
            if (!this.clubDraft.country) return this.cities;
            return this.cities.filter(c =>
                c.country.id === this.clubDraft.country.id
            )
        },
        hasMembershipErrors() {
            return this.membershipErrors.length > 0;
        }
    },
    watch: {
        'club': {
            handler(newClub) {
                if (newClub) {
                    this.clubDraft = { ...newClub }
                }
            },
            immediate: true
        },
    },
    methods: {
        async fetchClub() {
            try {
                this.errors = {}
                this.loading = true
                const res = await api.get(`/clubs/${this.id}/`)
                this.club = res.data
            } finally {
                this.loading = false
                this.checkMembership()
            }
        },
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
        cancel() {
            this.clubDraft = { ...this.club }
            this.editing = false
            this.errors = {}
        },
        async save() {
            try {
                this.loading = true
                this.errors = {}
                await api.patch(`/clubs/${this.id}/`, {
                    name: this.clubDraft.name,
                    country: (this.clubDraft.city && this.clubDraft.country) ? null : (this.clubDraft.country?.id || null),
                    city: this.clubDraft.city?.id || null,
                    contact_user: this.clubDraft.contact_user?.id || null
                })
                await this.fetchClub()
                this.hasSaved = true
                this.editing = false
            } catch (e) {
                this.errors = e.response?.data
            } finally {
                this.loading = false
            }
        },
        checkMembership() {
            if (this.club.members.find(m => m.user.id === this.authStore.user.id)) {
                this.isMember = true
            } else {
                this.isMember = false
            }
        },
        async joinClub() {
            try {
                this.membershipErrors = {}
                await api.post(`/clubs/${this.club.id}/members/`)
                this.isMember = true
                this.fetchClub()
            } catch (e) {
                this.membershipErrors = e.response?.data
            }
        },
        async leaveClub() {
            try {
                this.membershipErrors = []
                const membership_id = this.club.members.find(m => m.user.id === this.authStore.user.id)?.id
                await api.delete(`/clubs/${this.club.id}/members/${membership_id}/`)
                this.isMember = false
                this.fetchClub()
            } catch (e) {
                this.membershipErrors = e.response?.data
            }
        },
    },
    mounted() {
        this.fetchClub()
        this.fetchCities()
        this.fetchCountries()
        this.fetchUsers()
    },
}
</script>
<template>
    <v-sheet class="d-flex flex-column ga-6">
        <h1>{{ club.name }}</h1>
        <v-card :loading="loading">
            <v-card-actions v-if="authStore.user?.is_staff">
                <v-spacer></v-spacer>
                <v-btn variant="tonal" @click="editing ? cancel() : (editing = true)" width="80">
                    <v-fade-transition leave-absolute>
                        <span v-if="editing">Cancel</span>
                        <span v-else>Edit</span>
                    </v-fade-transition>
                </v-btn>
                <v-btn color="green" variant="tonal" :disabled="!editing" @click="save">Save</v-btn>
            </v-card-actions>

            <v-card-text>
                <v-text-field v-model="clubDraft.name" label="Name" :error-messages="errors.name"
                    :readonly="!editing"></v-text-field>
                <v-autocomplete v-model="clubDraft.country" :items="countries" item-title="name" label="Country"
                    return-object :error-messages="errors.country" :readonly="!editing"></v-autocomplete>
                <v-autocomplete v-model="clubDraft.city" :items="filteredCities" item-title="name" label="City"
                    return-object :error-messages="errors.city" :readonly="!editing"></v-autocomplete>
                <v-autocomplete v-model="clubDraft.contact_user" :items="users"
                    :item-title="user => `${user.first_name} ${user.last_name} (@${user.username})`"
                    label="Contact user" return-object :error-messages="errors.contact_user"
                    :readonly="!editing"></v-autocomplete>
                <p v-if="errors.non_field_errors?.length" class="mt-2 text-red-darken-2">
                    {{ errors.non_field_errors.join(' ') }}
                </p>
            </v-card-text>
            <v-snackbar v-model="hasSaved" color="green" :timeout="2000" location="bottom left">
                Club has been updated
            </v-snackbar>
        </v-card>
        <v-sheet v-if="authStore.isAuthenticated">
            <v-btn block v-if="isMember" variant="tonal" @click="leaveClub" color="black">
                Leave Club
            </v-btn>
            <v-btn block v-else variant="tonal" @click="joinClub" color="blue">
                Join club
            </v-btn>
        </v-sheet>
        <v-snackbar v-model="hasMembershipErrors" :timeout="2000" location="bottom left" color="red">
            {{ membershipErrors.join(" ") }}
        </v-snackbar>
    </v-sheet>
    <ClubMembersTable :club="club" @memberChanged="fetchClub" />
</template>
