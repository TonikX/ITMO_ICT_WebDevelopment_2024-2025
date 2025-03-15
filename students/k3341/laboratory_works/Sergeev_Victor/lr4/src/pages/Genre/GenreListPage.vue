<template>
<v-app>
    <v-banner><h1>Жанры</h1></v-banner>
    <v-btn @click="$router.push('/genre/create')">Добавить жанр</v-btn>
    <br>
    <v-btn @click="fetchGenres">Обновить жанры</v-btn>
    <div v-if="!isLoading">
    <transition-group name="genre-list">
        <genre-list
        :genres="genres"
        @remove_genre="deleteGenre"/>
    </transition-group>
    </div>
    <div v-else>
        Идёт загрузка
    </div>
</v-app>
</template>

<script>
import { onMounted, ref } from 'vue';
import GenreList from '@/components/Genre/GenreList.vue';
import instance from '@/AxiosInstance';
import { TokenStore } from '@/stores/TokenStore';
export default {
    components: {GenreList},
    setup() {
        const genres = ref([]);
        const isLoading = ref(false);
        const token = TokenStore();

        const fetchGenres = async () => {
            isLoading.value = true
            console.log(token.token);
            try {
                const response = await instance.get('/api/genre')
                genres.value = response.data;
            } catch(e) {
                console.log(e);
            } finally {
                isLoading.value = false;
            }
        };

        const deleteGenre = async (id) => {
            try {
                const response = await instance.delete('/api/genre/' + id + '/');
                if (response.status === 204) {
                    fetchGenres();
                }
            } catch (e) {
                console.log(e);
            }
        };

        onMounted(fetchGenres);

        return {
            genres,
            isLoading,
            fetchGenres,
            deleteGenre,
        };
    },
};
</script>

<style scoped>
</style>