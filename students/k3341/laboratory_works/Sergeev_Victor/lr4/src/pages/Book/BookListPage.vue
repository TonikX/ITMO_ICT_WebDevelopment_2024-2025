<template>
    <v-app>
    <v-banner><h1>Книги</h1></v-banner>
    <v-btn @click="$router.push('/book/create')">Создать книгу</v-btn>
    <br>
    <v-btn @click="fetchBooks">Загрузить книги</v-btn>
    <div v-if="!isLoading">
        <transition-group name="book-list">
            <book-list 
            :books="books"
            @remove_book="deleteBook"
            />
        </transition-group>
    </div>
    <div v-else>
        Идёт загрузка
    </div>
    </v-app>
</template>

<script>
import { onMounted, ref } from 'vue';
import BookList from '@/components/Book/BookList.vue';
import instance from '@/AxiosInstance';
export default {
    components: {BookList},
    setup() {
        const books = ref([]);
        const isLoading = ref(false);

        const fetchBooks = async () => {
            isLoading.value = true;
            try {
                const response = await instance.get('/api/book');
                books.value = response.data;
            } catch(e) {
                console.log(e);
            } finally {
                isLoading.value = false;
            }
        }
        
        const deleteBook = async (id) => {
            try {
                const response = await instance.delete('/api/book/' + id + '/')
                if (response.status === 204) {
                    fetchBooks();
                }
            } catch(e) {
                console.log(e);
            }
        }

        onMounted(fetchBooks);

        return {
            books,
            isLoading,
            fetchBooks,
            deleteBook
        }
    },
};
</script>

<style scoped>
</style>