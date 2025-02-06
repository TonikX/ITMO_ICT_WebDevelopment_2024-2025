<script>
import ParticipantsTable from '@/components/ParticipantsTable.vue';
import { api } from '@/utils/api';
import { useAuthStore } from '@/stores/auth';
import { mapStores } from 'pinia';


export default {
    components: {
        ParticipantsTable,
    },
    props: {
        id: String
    },
    data() {
        return {
            ascent: null,
            loading: false,

            isEditing: false,
            hasSaved: false,

            ascentDraft: {
                planned_start_datetime: '',
                planned_end_datetime: '',
                actual_start_datetime: '',
                actual_end_datetime: '',
                is_successful: false,
                summary: '',
                mountain: null,
                route: null,
            },
            errors: {},

            mountains: [],
            routes: [],

            isParticipant: false,
            participantsErrors: [],
        }
    },
    computed: {
        ...mapStores(useAuthStore),
        filteredRoutes() {
            if (!this.ascentDraft.mountain) return [];
            return this.routes.filter(route =>
                route.mountain.id === this.ascentDraft.mountain.id
            )
        },
        hasParticipantsErrors() {
            return this.participantsErrors.length > 0;
        }
    },
    watch: {
        'ascent': {
            handler(newAscent) {
                if (newAscent) {
                    this.ascentDraft = { ...newAscent }
                    this.formatAscentDates()
                }
            },
            immediate: true
        },
        // 'ascentDraft.mountain'(newVal) {
        //     if ((newVal.id !== this.ascentDraft.mountain) && this.isEditing) this.ascentDraft.route = null;
        // }
    },
    methods: {
        async fetchAscent() {
            try {
                this.errors = {}
                this.loading = true
                const res = await api.get(`/ascents/${this.id}/`)
                this.ascent = res.data
            } catch (e) {
                throw e
            } finally {
                this.loading = false
                this.checkParticipance()
            }
        },
        formatDateTime(isoDate) {
            if (!isoDate) return ""
            const date = new Date(isoDate)
            return date.toISOString().slice(0, 16)
        },
        formatAscentDates() {
            this.ascentDraft.planned_start_datetime = this.formatDateTime(this.ascentDraft.planned_start_datetime)
            this.ascentDraft.planned_end_datetime = this.formatDateTime(this.ascentDraft.planned_end_datetime)
            this.ascentDraft.actual_start_datetime = this.formatDateTime(this.ascentDraft.actual_start_datetime)
            this.ascentDraft.actual_end_datetime = this.formatDateTime(this.ascentDraft.actual_end_datetime)
        },
        async fetchMountainsAndRoutes() {
            try {
                this.loading = true
                const mountainsRes = await api.get("/mountains/")
                this.mountains = mountainsRes.data
                const routesRes = await api.get("/routes/")
                this.routes = routesRes.data
            } catch (e) {
                throw e
            } finally {
                this.loading = false
            }
        },
        cancel() {
            this.ascentDraft = { ...this.ascent };
            this.formatAscentDates()
            this.isEditing = false;
            this.errors = {}
        },
        async save() {
            this.errors = {}
            try {
                this.loading = true
                const payload = {
                    planned_start_datetime: this.ascentDraft.planned_start_datetime,
                    planned_end_datetime: this.ascentDraft.planned_end_datetime,
                    actual_start_datetime: this.ascentDraft.actual_start_datetime || null,
                    actual_end_datetime: this.ascentDraft.actual_end_datetime || null,
                    is_successful: this.ascentDraft.is_successful,
                    summary: this.ascentDraft.summary,
                    route: this.ascentDraft.route.id || this.ascentDraft.route,
                }
                const res = await api.patch(`/ascents/${this.id}/`, payload)
                await this.fetchAscent()

                this.hasSaved = true
                this.isEditing = false
            } catch (err) {
                this.errors = err.response?.data
            } finally {
                this.loading = false
            }
        },

        checkParticipance() {
            if (this.ascent.participants.find(p => p.user.id === this.authStore.user.id)) {
                this.isParticipant = true
            } else {
                this.isParticipant = false
            }
        },
        async participate() {
            try {
                this.participantsErrors = []
                await api.post(`/ascents/${this.ascent.id}/participants/`)
                this.isParticipant = true
                this.fetchAscent()
            } catch (e) {
                this.participantsErrors = e.response?.data
            }
        },
        async leave() {
            try {
                this.participantsErrors = []
                const participation_id = this.ascent.participants.find(p => p.user.id === this.authStore.user.id)?.id
                await api.delete(`/ascents/${this.ascent.id}/participants/${participation_id}/`)
                this.isParticipant = false
                this.fetchAscent()
            } catch (e) {
                this.participantsErrors = e.response?.data
            }
        },
    },
    mounted() {
        this.fetchAscent()
        this.fetchMountainsAndRoutes()
    },
}
</script>
<template>
    <v-sheet class="d-flex flex-column ga-6">
        <h1>Acent Details</h1>
        <v-card :loading="loading">
            <v-card-actions v-if="authStore.user?.is_staff">
                <v-spacer></v-spacer>
                <v-btn variant="tonal" @click="isEditing ? cancel() : (isEditing = true)" width="80">
                    <v-fade-transition leave-absolute>
                        <span v-if="isEditing">Cancel</span>
                        <span v-else>Edit</span>
                    </v-fade-transition>
                </v-btn>
                <v-btn color="green" variant="tonal" :disabled="!isEditing" @click="save">Save</v-btn>
            </v-card-actions>

            <v-card-text>
                <v-row>
                    <v-col>
                        <v-text-field v-model="ascentDraft.planned_start_datetime" label="Planned Start"
                            type="datetime-local" :error-messages="errors.planned_start_datetime"
                            :readonly="!isEditing"></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field v-model="ascentDraft.actual_start_datetime" label="Actual Start"
                            type="datetime-local" :error-messages="errors.actual_start_datetime"
                            :readonly="!isEditing"></v-text-field>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-text-field v-model="ascentDraft.planned_end_datetime" label="Planned End"
                            type="datetime-local" :error-messages="errors.planned_end_datetime"
                            :readonly="!isEditing"></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field v-model="ascentDraft.actual_end_datetime" label="Actual End" type="datetime-local"
                            :error-messages="errors.actual_end_datetime" :readonly="!isEditing"></v-text-field>
                    </v-col>
                </v-row>

                <v-autocomplete v-model="ascentDraft.mountain" :items="mountains" item-value="id" item-title="name"
                    label="Mountain" return-object :readonly="!isEditing" />

                <v-autocomplete v-model="ascentDraft.route" :items="filteredRoutes" item-value="id" item-title="name"
                    label="Route" :disabled="!ascentDraft.mountain" :error-messages="errors.route"
                    :readonly="!isEditing" />

                <v-checkbox v-model="ascentDraft.is_successful" label="Successful" :readonly="!isEditing"></v-checkbox>
                <v-textarea v-model="ascentDraft.summary" label="Summary" :readonly="!isEditing"></v-textarea>
            </v-card-text>

            <v-snackbar v-model="hasSaved" :timeout="2000" location="bottom left">
                Ascent has been updated
            </v-snackbar>

        </v-card>
        <v-sheet v-if="authStore.isAuthenticated">
            <v-btn block v-if="isParticipant" variant="tonal" @click="leave" color="black">
                Leave
            </v-btn>
            <v-btn block v-else variant="tonal" @click="participate" color="blue">
                Participate
            </v-btn>

        </v-sheet>
        <v-snackbar v-model="hasParticipantsErrors" :timeout="2000" location="bottom left" color="red">
            {{ participantsErrors.join(" ") }}
        </v-snackbar>
        <ParticipantsTable :ascent="ascent" @participantChanged="fetchAscent" />
    </v-sheet>
</template>