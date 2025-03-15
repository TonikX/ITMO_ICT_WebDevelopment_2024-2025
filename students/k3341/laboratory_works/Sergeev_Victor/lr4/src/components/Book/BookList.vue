<template>
    <div v-if="books.length > 0">
        <transition-group name="book-list">
            <book-list-item v-for="book in books"
            :book="book"
            :key="book.id"
            @remove_book="$emit('remove_book', book.id)"
            />
        </transition-group>
    </div>
    <div v-else style="color: red">
        Нет книг
    </div>
</template>

<script>
import BookListItem from './BookListItem.vue';

export default {
    components: {BookListItem},
    props: {
        books: {
            type: Array,
            required: true,
        }
    }
}
</script>

<style scoped>

</style>