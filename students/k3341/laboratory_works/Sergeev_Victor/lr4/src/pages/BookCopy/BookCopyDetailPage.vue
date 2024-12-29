<template>
<v-app>
    <div class="book-copy-box">
        <v-banner><h1>{{ book_copy.book.title }}</h1></v-banner>
        <v-banner>Издательство: {{ book_copy.book.publisher }}</v-banner>
        <v-banner>Год издания: {{ book_copy.publish_year }}</v-banner>
        <v-banner>Шифр копии: {{ book_copy.cipher }}</v-banner>
    </div>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
    setup() {
        const book_copy = ref({
            cipher: '',
            publish_year: '',
            book: {}
        })
        const id = useRoute().params.id;

        const fetchBookCopy = async () => {
            try {
                const response = await instance.get('/api/book_copy/' + id);
                book_copy.value = response.data;
            } catch (e) {
                console.log(e);
            }
        }

        onMounted(fetchBookCopy);

        return {
            book_copy,
            fetchBookCopy,
        }
    }
}
</script>

<style scoped>
.book-copy-box {
    padding: 15px;
    margin-top: 20px;
}

</style>