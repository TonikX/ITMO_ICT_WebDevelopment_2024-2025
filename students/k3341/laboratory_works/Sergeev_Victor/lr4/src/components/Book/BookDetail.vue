<template>
    <div class="book-box">
        <!-- <button @click="$router.push(`/book/${book.id}/add_genre`)">Добавить жанр</button>
        <button @click="$router.push(`/book/${book.id}/add_author`)">Добавить автора</button> -->
        <div class="book-title">
            <h1>{{ book.title }}</h1>
        </div>
        <div class="book-publisher">
            Издательство: {{ book.publisher }}
        </div>
        <div class="book-authors">
            <transition-group name='book-author-list'>
                <author-list :authors="book.authors"/>
            </transition-group>
        </div>
        <div class="book-genres">
            <transition-group name="book-genre-list">
                <genre-list :genres="book.genres"/>
            </transition-group>
        </div>
    </div>
</template>

<script>
import AuthorList from '../Author/AuthorList.vue';
import GenreList from '../Genre/GenreList.vue';
export default {
    components: {AuthorList, GenreList},
    props: {
        book: {
            type: Object,
            required: true,
        }
    },
    data() {
        return {
            book: {
                title: "my first book",
                publisher: "izdatelstvo",
                authors: [
                    {"id": 1, "full_name": "author1"},
                    {"id": 2, "full_name": "author2"},
                    {"id": 3, "full_name": "author3"},
                ],
                genres: [
                    {"id": 1, "title": "genre_1"},
                    {"id": 2, "title": "genre_2"},
                    {"id": 3, "title": "genre_3"},
                    {"id": 4, "title": "genre_4"},
                ],
            }
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