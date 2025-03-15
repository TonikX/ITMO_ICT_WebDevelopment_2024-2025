<template>
<v-app>
    <div class="book-copy-form">
        <v-form @submit.prevent="createBookCopy">
            <v-text-field label="ID книги" v-model="bookCopy.book"></v-text-field>
            <v-text-field label="Шифр книги" v-model="bookCopy.cipher"></v-text-field>
            <v-text-field label="Год публикации" v-model="bookCopy.publish_year"></v-text-field>
            <v-btn type="submit">Создать копию книги</v-btn>
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
        const bookCopy = ref({
            book: '',
            cipher: '',
            publish_year: new Date().getFullYear(),
        });

        const createBookCopy = async () => {
            try {
                const response = await instance.post('/api/book_copy/create/', bookCopy.value);
                if (response.status === 201) {
                    router.push('/book_copy');
                }
            } catch (e) {
                console.log(e);
            }
        };

        return {
            bookCopy,
            createBookCopy,
        }
    }
}
</script>

<style scoped>
</style>