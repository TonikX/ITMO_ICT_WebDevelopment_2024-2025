<script>
import { api } from '@/utils/api';
import CreateClub from '@/components/CreateClub.vue';

export default {
    components: { CreateClub },
    data() {
        return {
            clubs: [],
            loading: false,
            headers: [
                { title: "Club", key: "name", value: "name" },
                { title: "Country", key: "country.id", value: "country.name" },
                { title: "City", key: "city.id", value: "city.name" },
                { title: "No. members", key: "members", value: item => `${item.members.length}` },
            ]
        }
    },
    methods: {
        async fetchClubs() {
            try {
                this.loading = true
                const res = await api.get('/clubs/', { params: { ordering: '-id' } })
                this.clubs = res.data
            } finally {
                this.loading = false
            }
        },
        handleRowClick(event, { item }) {
            this.$router.push(`/clubs/${item.id}`)
        },
    },
    mounted() {
        this.fetchClubs()
    },

}
</script>

<template>
    <h1>Clubs</h1>
    <CreateClub @clubCreated="fetchClubs" />
    <v-data-table :loading="loading" :headers="headers" :items="clubs" @click:row="handleRowClick">
    </v-data-table>
</template>