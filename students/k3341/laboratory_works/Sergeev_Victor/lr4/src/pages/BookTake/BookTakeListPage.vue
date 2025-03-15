<template>
<v-app>
    <v-banner><h1>Взятия и возвраты книг</h1></v-banner>
    <v-btn @click="$router.push('/book_take/create')">Выдать книгу</v-btn>
    <br>
    <v-btn @click="fetchBookTakes">Загрузить выдачи книг</v-btn>
    <div v-if="!isLoading">
        <transition-group name="book-take-list">
            <book-take-list
            :book_takes="book_takes"
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
import BookTakeList from '@/components/BookTake/BookTakeList.vue';
import instance from '@/AxiosInstance';
import { useRoute } from 'vue-router';
export default {
    components: {BookTakeList},
    setup() {
        const book_takes = ref([]);
        const isLoading = ref(false);
        const id = useRoute().params.id;
        
        const fetchBookTakes = async () => {
            isLoading.value = true;
            try {
                console.log(book_takes.value)
                const response = await instance.get('/api/reader/' + id + '/book');
                book_takes.value = response.data;
            } catch(e) {
                console.log(e);
            } finally {
                isLoading.value = false;
            }
        };

        onMounted(fetchBookTakes);

        return {
            book_takes,
            isLoading,
            fetchBookTakes,
        };
    },
};
</script>

<style scoped>

</style>