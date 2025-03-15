<template>
<v-app>
    <div class="book-box">
        <v-btn @click="$router.push(`/book/${book.id}/add_genre`)">Добавить жанр</v-btn>
        <v-btn @click="$router.push(`/book/${book.id}/add_author`)">Добавить автора</v-btn>
        <br>
        <v-text-field label="Название" v-model="book.title"></v-text-field>
        <v-text-field label="Издательство" v-model="book.publisher"></v-text-field>

        <v-btn @click="saveBook">Сохранить</v-btn>
        <div class="book-authors">
            <h3>Авторы</h3>
            <transition-group name='book-author-list'>
                <author-list
                :authors="book.author"
                @remove_author="deleteAuthor"
                />
            </transition-group>
        </div>
        <h3>Жанры</h3>
        <div class="book-genres">
            <transition-group name="book-genre-list">
                <genre-list
                :genres="book.genre"
                @remove_genre="deleteGenre"
                />
            </transition-group>
        </div>
    </div>
</v-app>
</template>

<script>
import { onMounted, ref } from 'vue';
import AuthorList from '@/components/Author/AuthorList.vue';
import GenreList from '@/components/Genre/GenreList.vue';
import { useRoute } from 'vue-router';
import instance from '@/AxiosInstance';
export default {
    components: {AuthorList, GenreList},
    setup() {
        const book = ref({
            title: '',
            publisher: '',
            genre: [],
            author: []
        });
        const id = useRoute().params.id;
        
        const fetchBook = async () => {
            try {
                const response = await instance.get('/api/book/' + id);
                book.value = response.data;
            } catch (e) {
                console.log(e)
            }
        };

        const saveBook = async () => {
            try {
                const response = await instance.patch('/api/book/' + id + '/', book.value);
                if (response.status == 200) {
                    alert('updated successfully');
                }
            } catch (e) {
                console.log(e);
            }
        };

        const deleteAuthor = async (author_id) => {
            try {
                const response = await instance.delete('/api/book_author/' + id + '/?author_id=' + author_id)
                if (response.status === 204) {
                    alert('deleted successfully')
                    fetchBook();
                }
            } catch (e) {
                console.log(e)
            }
        };

        const deleteGenre = async (genre_id) => {
            console.log('here')
            try {
                const response = await instance.delete('/api/book_genre/' + id + '/?genre_id=' + genre_id)
                if (response.status === 204) {
                    alert('deleted successfully');
                    fetchBook();
                }
            } catch (e) {
                console.log(e)
            }
        };

        onMounted(fetchBook);

        return {
            book,
            fetchBook,
            saveBook,
            deleteAuthor,
            deleteGenre,
        }
    }
}
</script>

<style scoped>
.book-box {
    padding: 15px;
    margin-top: 20px;
}

</style>