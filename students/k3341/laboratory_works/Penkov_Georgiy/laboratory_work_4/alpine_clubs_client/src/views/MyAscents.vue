<script>
import { api } from '@/utils/api';

export default {
    data() {
        return {
            ascents: [],
            loading: false,

            headers: [
                {
                    title: "Date",
                    align: 'center',
                    children: [
                        {
                            title: "Planned start",
                            key: "ascent.planned_start_datetime",
                            value: item => new Date(item.ascent.planned_start_datetime).toLocaleDateString("ru-RU")
                        },
                        {
                            title: "Planned end",
                            key: "ascent.planned_end_datetime",
                            value: item => new Date(item.ascent.planned_end_datetime).toLocaleDateString("ru-RU")
                        },
                    ]
                },

                { title: "Mountain", key: "ascent.mountain.id", value: "ascent.mountain.name" },
                { title: "Route", key: "ascent.route.id", value: "ascent.route.name" },
                { title: "No. participants", key: "participants", value: item => `${item.ascent.participants.length}` },
                { title: "Status", key: "ascent_status" },
                {
                    title: "Personal Status",
                    align: 'center',
                    children: [
                        {
                            title: "Successful",
                            key: "personal_is_successful",
                        },
                        {
                            title: "Incident",
                            key: "incident_type",
                        },
                    ]
                },

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
        }
    },
    methods: {
        async fetchAscents() {
            try {
                this.loading = true
                const res = await api.get('/ascents/me/')
                this.ascents = res.data
            } finally {
                this.loading = false
            }
        },
        handleRowClick(event, { item }) {
            this.$router.push(`/ascents/${item.ascent.id}`)
        },
    },
    mounted() {
        this.fetchAscents()
    }
}
</script>

<template>
    <h2>My Ascents</h2>
    <v-data-table :loading="loading" :headers="headers" :items="ascents" @click:row="handleRowClick">
        <template v-slot:loading>
            <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>
        <template v-slot:item.ascent_status="{ item }">
            <v-chip :color="item.is_successful ? 'green' : 'grey'" class="text-white">
                {{ item.is_successful ? "Success" : "N/A" }}
            </v-chip>
        </template>
        <template v-slot:item.personal_is_successful="{ item }">
            <v-chip :color="item.personal_is_successful ? 'green' : 'grey'" class="text-white">
                {{ item.personal_is_successful ? "Yes" : "No" }}
            </v-chip>
        </template>
        <template v-slot:item.incident_type="{ item }">
            <v-chip :color="item.incident_type ? 'black' : 'grey'">
                {{ this.incidentTypes.find(t => t.key === item.incident_type)?.label || "None" }}
            </v-chip>
        </template>
    </v-data-table>
</template>