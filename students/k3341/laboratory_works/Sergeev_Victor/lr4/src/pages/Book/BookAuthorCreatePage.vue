<template>
<v-app>
    <v-form @submit.prevent="addAuthor">
        <v-text-field label="ID автора" v-model="book_author.author"></v-text-field>
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
        const book_author = ref({
            book: book_id,
            author: ''
        });

        const addAuthor = async () => {
            try {
                const response = await instance.post('/api/book_author/', book_author.value)
                if (response.status === 201) {
                    router.push('/book/' + book_id);
                }
            } catch (e) {
                console.log(e)
            };
        }

        return {
            book_author,
            addAuthor,
        }
    }
}
</script>

<style scoped>
</style>