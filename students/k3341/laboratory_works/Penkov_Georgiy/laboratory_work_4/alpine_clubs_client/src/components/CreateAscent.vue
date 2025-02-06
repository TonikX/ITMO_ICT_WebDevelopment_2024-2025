<script>
import { useAuthStore } from '@/stores/auth';
import { mapStores } from 'pinia';
import { api } from '@/utils/api';

export default {
    emits: ['ascentCreated'],
    data() {
        return {
            dialog: false,
            newAscent: {
                planned_start_datetime: '',
                planned_end_datetime: '',
                mountain: null,
                route: null,
            },
            mountains: [],
            routes: [],

            loading: false,
            errors: [],
        }
    },
    computed: {
        ...mapStores(useAuthStore),
        filteredRoutes() {
            if (!this.newAscent.mountain) return [];
            return this.routes.filter(route =>
                route.mountain.id === this.newAscent.mountain.id
            );
        }
    },
    methods: {
        async fetchMountainsAndRoutes() {
            try {
                const mountainsRes = await api.get("/mountains/");
                this.mountains = mountainsRes.data;
                const routesRes = await api.get("/routes/");
                this.routes = routesRes.data;
            } catch (e) {
                throw e
            }
        },
        async createAscent() {
            try {
                this.loading = true
                this.errors = {}
                await api.post("/ascents/", {
                    planned_start_datetime: this.newAscent.planned_start_datetime,
                    planned_end_datetime: this.newAscent.planned_end_datetime,
                    route: this.newAscent.route,
                })
                this.newAscent = {}
                this.dialog = false
                this.$emit('ascentCreated')
            } catch (e) {
                this.errors = e.response?.data
            } finally {
                this.loading = false
            }
        },
    },
    watch: {
        'newAscent.mountain'(newVal) {
            if (newVal) this.newAscent.route = null
        }
    },
    mounted() {
        this.fetchMountainsAndRoutes();
    },

}
</script>

<template>
    <v-dialog v-model="dialog" max-width="500">

        <template v-slot:activator="{ props: activatorProps }">
            <v-btn v-if="authStore.user?.is_staff" @click="dialog = true" prepend-icon="mdi-plus"
                v-bind="activatorProps" variant="tonal" color="blue" block>New Ascent</v-btn>
        </template>

        <v-card class="pa-4" :loading="loading">
            <v-card-title>Create New Ascent</v-card-title>

            <v-card-text>

                <v-text-field v-model="newAscent.planned_start_datetime" label="Planned Start" type="datetime-local"
                    clearable :error-messages="errors.planned_start_datetime"></v-text-field>

                <v-text-field v-model="newAscent.planned_end_datetime" label="Planned End" type="datetime-local"
                    clearable :error-messages="errors.planned_end_datetime"></v-text-field>

                <v-autocomplete v-model="newAscent.mountain" :items="mountains" item-value="id" item-title="name"
                    label="Mountain" return-object />

                <v-autocomplete v-model="newAscent.route" :items="filteredRoutes" item-value="id" item-title="name"
                    label="Route" :disabled="!newAscent.mountain" :error-messages="errors.route" />

            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn variant="tonal" @click="dialog = false">Cancel</v-btn>
                <v-btn variant="tonal" @click="createAscent">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>