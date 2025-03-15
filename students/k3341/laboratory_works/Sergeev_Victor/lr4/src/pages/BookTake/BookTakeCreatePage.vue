<template>
<v-app>
    <div class="book-take-create-form">
        <v-form @submit.prevent="createBookTake">
            <v-text-field label="ID копии" v-model="bookTake.book_copy"></v-text-field>
            <v-text-field label="ID читателя" v-model="bookTake.reader"></v-text-field>
            <v-text-field label="Дата взятия" v-model="bookTake.take_date"></v-text-field>
            <v-btn type="submit">Добавить</v-btn>
        </v-form>
    </div>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import router from '@/router';
import { ref } from 'vue';

export default {
    setup () {
        const bookTake = ref({
            book_copy: '',
            reader: '',
            take_date: '',
        })

        const createBookTake = async () => {
            try {
                const response = await instance.post('/api/book_take/create/', bookTake.value);
                if (response.status == 201) {
                    router.push('/reader/' + bookTake.value.reader);
                }
            } catch (e) {
                console.log(e);
            }
        }

        return {
            bookTake,
            createBookTake,
        }
    }
}
</script>

<style scoped>
</style>