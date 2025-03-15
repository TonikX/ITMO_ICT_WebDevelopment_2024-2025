<template>
<v-app>
    <v-banner><h1>Копии книг</h1></v-banner>
    <v-btn @click="$router.push('/book_copy/create')">Зарегистрировать копию книги</v-btn>
    <br>
    <v-btn @click="fetchBookCopies">Загрузить копии</v-btn>
    <div v-if="!isLoading">
        <transition-group name="book-copy-list">
            <book-copy-list
            :book_copies="book_copies"
            @remove_copy="deleteBookCopy"/>
        </transition-group>
    </div>
    <div v-else>
        Идёт загрузка
    </div>
</v-app>
</template>

<script>
import { onMounted, ref } from 'vue';
import BookCopyList from '@/components/BookCopy/BookCopyList.vue';
import instance from '@/AxiosInstance';
export default {
    components: {BookCopyList},
    setup() {
        const book_copies = ref([]);
        const isLoading = ref(false);

        const fetchBookCopies = async () => {
            isLoading.value = true;
            try {
                const response = await instance.get('/api/book_copy');
                book_copies.value = response.data;
            } catch(e) {
                console.log(e)
            } finally {
                isLoading.value = false;
            }
        }

        const deleteBookCopy = async (id) => {
            try {
                const response = await instance.delete('/api/book_copy/' + id + '/');
                if (response.status === 204) {
                    fetchBookCopies();
                }
            } catch(e) {
                console.log(e)
            }
        }

        onMounted(fetchBookCopies)
        return {
            book_copies,
            isLoading,
            fetchBookCopies,
            deleteBookCopy,
        };
    },
};
</script>

<style scoped>
</style>