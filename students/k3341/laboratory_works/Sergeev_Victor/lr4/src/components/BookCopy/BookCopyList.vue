<template>
    <div v-if="book_copies.length > 0">
        <transition-group name="book-list">
            <book-copy-list-item v-for="book_copy in book_copies"
            :book_copy="book_copy"
            :key="book_copy.id"
            @remove_copy="$emit('remove_copy', book_copy.id)"
            />
        </transition-group>
    </div>
    <div v-else style="color: red">
        Нет копий книг
    </div>
</template>

<script>
import BookCopyListItem from './BookCopyListItem.vue';
export default {
    components: {BookCopyListItem},
    props: {
        book_copies: {
            type: Array,
            required: true,
        }
    }
}
</script>

<style scoped>

</style>