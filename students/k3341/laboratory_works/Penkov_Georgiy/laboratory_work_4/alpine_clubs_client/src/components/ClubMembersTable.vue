<script>
import { mapStores } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import { api } from '@/utils/api';

export default {
    props: {
        club: Object,
    },
    emits: ['memberChanged'],
    computed: {
        ...mapStores(useAuthStore),
    },
    data() {
        return {
            loading: false,
            headers: [
                { title: "Member", key: "user.id", value: (m) => `${m.user.first_name} ${m.user.last_name}` },
                { title: "Joined", key: "join_datetime", value: (item) => new Date(item.join_datetime).toLocaleDateString("ru-RU") },
                { title: "Actions", key: 'actions' },
            ],
            dialogDelete: false,
            item_id: null,
        };
    },
    methods: {
        handleDelete(item) {
            this.dialogDelete = true
            this.item_id = item.id
        },
        async performDelete() {
            try {
                const res = await api.delete(`/clubs/${this.club.id}/members/${this.item_id}/`)
                this.$emit('memberChanged')
                this.dialogDelete = false
            } catch (e) {
                throw e
            }
        }
    },
};
</script>

<template>
    <h2>Members</h2>
    <v-data-table :headers="headers" :items="club.members" :loading="loading">
        <template v-slot:item.actions="{ item }" v-if="authStore.user?.is_staff">
            <v-icon @click="handleDelete(item)">
                mdi-delete
            </v-icon>
        </template>
    </v-data-table>
    <v-dialog v-model="dialogDelete" max-width="500">
        <v-card class="pa-4">
            <v-card-title>Delete member?</v-card-title>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn variant="tonal" @click="dialogDelete = false">Cancel</v-btn>
                <v-btn variant="tonal" @click="performDelete">OK</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>