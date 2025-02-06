<script>
import { mapStores } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import { api } from '@/utils/api';

export default {
    data() {
        return {
            ascents: [],
            loading: false,
            sortBy: [{ key: 'planned_start_datetime', order: 'desc' }],
            headers: [
                {
                    title: "Date",
                    align: 'center',
                    children: [
                        {
                            title: "Planned start",
                            key: "planned_start_datetime",
                        },
                        {
                            title: "Planned end",
                            key: "planned_end_datetime",
                        },
                    ]
                },

                { title: "Mountain", key: "mountain.id", value: "mountain.name" },
                { title: "Route", key: "route.id", value: "route.name" },
                { title: "No. participants", key: "participants", value: item => `${item.participants.length}` },
                { title: "Status", key: "status" },
            ],
        }
    },
    computed: {
        ...mapStores(useAuthStore)
    },
    methods: {
        async fetchAscents() {
            try {
                this.loading = true
                const res = await api.get('/ascents/', { params: { ordering: '-id' } })
                this.ascents = res.data

            } catch (e) {
                throw e
            } finally {
                this.loading = false
            }
        },
        handleRowClick(event, { item }) {
            this.$router.push(`/ascents/${item.id}`)
        },
    },
    mounted() {
        this.fetchAscents()
    },

}
</script>

<template>
    <v-data-table :group-by="[{ key: 'mountain.name', order: 'asc' }]" :headers="headers" :items="ascents"
        :loading="loading" @click:row="handleRowClick" v-model:sort-by="sortBy">
        <template v-slot:loading>
            <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>
        <template v-slot:item.planned_start_datetime="{ item }">
            {{ new Date(item.planned_start_datetime).toLocaleDateString("ru-RU") }}
        </template>
        <template v-slot:item.planned_end_datetime="{ item }">
            {{ new Date(item.planned_end_datetime).toLocaleDateString("ru-RU") }}
        </template>
        <template v-slot:item.status="{ item }">
            <v-chip :color="item.is_successful ? 'green' : 'grey'" class="text-white">
                {{ item.is_successful ? "Success" : "N/A" }}
            </v-chip>
        </template>
    </v-data-table>
</template>