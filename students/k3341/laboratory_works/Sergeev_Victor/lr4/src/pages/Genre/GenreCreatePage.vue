<template>
<v-app>
    <div class="reader-create-form">
        <v-form @submit.prevent="createGenre">
            <v-text-field label="Название жанра" v-model="genre.title"></v-text-field>
            <v-btn type="submit">Создать жанр</v-btn>
        </v-form>
    </div>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import router from '@/router';
import { ref } from 'vue';

export default {
    setup() {
        const genre = ref({
            title: ''
        })

        const createGenre = async () => {
            console.log(genre.value)
            try {
                const response = await instance.post('/api/genre/create', genre.value);
                if (response.status === 201) {
                    router.push('/genre')
                }
            } catch(e) {
                console.log(e)
            };
        }

        return {
            genre,
            createGenre,
        }
    },
};
</script>

<style scoped>

</style>