<template>
    <div v-if="book_takes.length > 0">
        <transition-group name="book-take-list">
            <book-take-list-item v-for="book_take in book_takes"
            :book_take="book_take"
            :key="book_take.id"
            />
        </transition-group>
    </div>
    <div v-else style="color: red">
        Нет выданных книг
    </div>
</template>

<script>
import BookTakeListItem from './BookTakeListItem.vue';
export default {
    components: {BookTakeListItem},
    props: {
        book_takes: {
            type: Array,
            required: true,
        }
    }
};
</script>

<style scoped>

</style>