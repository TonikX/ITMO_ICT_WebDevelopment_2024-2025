<template>
<v-app>
    <v-form @submit.prevent="addGenre">
        <v-text-field label="ID жанра" v-model="book_genre.genre"></v-text-field>
        <v-btn type="submit">Добавить</v-btn>
    </v-form>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import router from '@/router';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
    setup() {
        const book_id = useRoute().params.id
        const book_genre = ref({
            book: book_id,
            genre: ''
        });

        const addGenre = async () => {
            try {
                const response = await instance.post('/api/book_genre/', book_genre.value)
                if (response.status === 201) {
                    router.push('/book/' + book_id);
                }
            } catch (e) {
                console.log(e)
            };
        }

        return {
            book_genre,
            addGenre,
        }
    }
}
</script>

<style scoped>
</style>