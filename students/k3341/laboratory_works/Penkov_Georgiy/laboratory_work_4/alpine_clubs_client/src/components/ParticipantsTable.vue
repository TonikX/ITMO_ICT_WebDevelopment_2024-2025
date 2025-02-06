<script>
import { api } from '@/utils/api';
import { useAuthStore } from '@/stores/auth';
import { mapStores } from 'pinia';


export default {
    props: {
        ascent: Object,
    },
    emits: ['participantChanged'],
    computed: {
        ...mapStores(useAuthStore),
    },
    data() {
        return {
            loading: false,
            headers: [
                { title: "User", key: "user.id", value: (p) => `${p.user.first_name} ${p.user.last_name}` },
                { title: "Club", key: "user.club.id", value: "user.club.name" },
                { title: "Successful", key: "is_successful" },
                { title: "Incident", key: "incident_type" },
                { title: "Incident Details", key: "incident_details" },
                { title: "Actions", key: 'actions' }
            ],
            incidentTypes: [
                {
                    key: "INJ",
                    label: "Injured",
                },
                {
                    key: "MIS",
                    label: "Missing",
                },
                {
                    key: "FAT",
                    label: "Fatality",
                },
            ],
            dialog: false,
            dialogDelete: false,

            item_id: null,
            editedItem: {
                is_successful: false,
                incident_type: null,
                incident_details: '',
            },
        }
    },
    methods: {
        handleEdit(item) {
            this.dialog = true
            this.item_id = item.id
            this.editedItem = { ...item }
        },
        async performEdit() {
            try {
                const res = await api.patch(`/ascents/${this.ascent.id}/participants/${this.item_id}/`, { ...this.editedItem })
                this.editedItem = { ...res.data }
                this.$emit('participantChanged')
                this.dialog = false
            } catch (e) {
                throw e
            }
        },
        handleDelete(item) {
            this.dialogDelete = true
            this.item_id = item.id
        },
        async performDelete() {
            try {
                const res = await api.delete(`/ascents/${this.ascent.id}/participants/${this.item_id}/`)
                this.$emit('participantChanged')
                this.dialogDelete = false
            } catch (e) {
                throw e
            }
        }
    },

}
</script>

<template>
    <h2>Participants</h2>
    <v-data-table :loading="loading" :headers="headers" :items="ascent?.participants">
        <template v-slot:item.is_successful="{ item }">
            <v-chip :color="item.is_successful ? 'green' : 'grey'" class="text-white">
                {{ item.is_successful ? "Yes" : "No" }}
            </v-chip>
        </template>
        <template v-slot:item.incident_type="{ item }">
            <v-chip :color="item.incident_type ? 'black' : 'grey'">
                {{ this.incidentTypes.find(t => t.key === item.incident_type)?.label || "None" }}
            </v-chip>
        </template>
        <template v-slot:item.actions="{ item }" v-if="authStore.user?.is_staff">
            <v-icon class="me-6" @click="handleEdit(item)">
                mdi-pencil
            </v-icon>
            <v-icon @click="handleDelete(item)">
                mdi-delete
            </v-icon>
        </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500">
        <v-card class="pa-4">
            <v-card-title>Edit participant</v-card-title>
            <v-card-text>
                <v-checkbox v-model="editedItem.is_successful" label="Successful"></v-checkbox>
                <h1 class="text-h6">Incident</h1>
                <v-select v-model="editedItem.incident_type" label="Type (if any)" :items="incidentTypes"
                    item-title="label" item-value="key" clearable></v-select>
                <v-textarea v-model="editedItem.incident_details" label="Details"></v-textarea>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="red" variant="tonal" @click="dialog = false">Cancel</v-btn>
                <v-btn color="green" variant="tonal" @click="performEdit">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

    <v-dialog v-model="dialogDelete" max-width="500">
        <v-card class="pa-4">
            <v-card-title>Delete participant?</v-card-title>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn variant="tonal" @click="dialogDelete = false">Cancel</v-btn>
                <v-btn variant="tonal" @click="performDelete">OK</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>