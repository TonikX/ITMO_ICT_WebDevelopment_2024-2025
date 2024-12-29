<template>
    <v-app>
    <div class="book-take-box">
        <v-text-field label="ID копии книги" v-model="book_take.book_copy"></v-text-field>
        <v-text-field label="ID читателя" v-model="book_take.reader"></v-text-field>
        <v-text-field label="Дата взятия" v-model="book_take.take_date"></v-text-field>
        <v-text-field label="Дата возврата" v-model="book_take.restore_date"></v-text-field>
    </div>
    <v-btn @click="saveBookTake">Сохранить</v-btn>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
    setup() {
        const book_take = ref({});
        const id = useRoute().params.id;
        
        const fetchBookTake = async () => {
            try {
                const response = await instance.get('/api/book_take/' + id);
                book_take.value = response.data;
            } catch (e) {
                console.log(e);
            }
        }

        const saveBookTake = async () => {
            try {
                const response = await instance.patch('/api/book_take/' + id + '/', book_take.value);
                if (response.status === 200) {
                    alert('updated successfully');
                }
            } catch (e) {
                console.log(e);
            }
        }

        onMounted(fetchBookTake);

        return {
            book_take,
            fetchBookTake,
            saveBookTake,
        }
    }
}
</script>

<style scoped>
</style>