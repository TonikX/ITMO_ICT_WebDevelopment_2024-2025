<template>
<v-app>
    <div class="book-create-form">
        <v-form @submit.prevent="createBook">
            <v-text-field label="Название" v-model="book.title"></v-text-field>
            <v-text-field label="Издательство" v-model="book.publisher"></v-text-field>
            <v-btn type="submit">Создать книгу</v-btn>
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
        const book = ref({
            title: '',
            publisher: '',
            genre: [],
            author: [],
        });

        const createBook = async () => {
            try {
                const response = await instance.post('/api/book/create/', book.value)
                if (response.status == 201) {
                    router.push('/book');
                }
            } catch(e) {
                console.log(e);
            }
        };

        return {
            book,
            createBook,
        }
    },
};
</script>

<style scoped>
</style>