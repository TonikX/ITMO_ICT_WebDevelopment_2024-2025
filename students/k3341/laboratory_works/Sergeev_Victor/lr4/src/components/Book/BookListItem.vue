<template>
    <div class="book-box">
        <div class="book-title">
            <router-link
                :to="{path: `/book/${book.id}`}">
                {{ book.title }}
            </router-link>
        </div>
        <div class="book-publisher">
            Издательство: {{ book.publisher }}
        </div>
        <br>
        <button class="delete-button"
            @click="$emit('remove_book', book)"
            style="color: red;">
            Удалить
        </button>
    </div>
</template>

<script>
export default {
    props: {
        book: {
            type: Object,
            required: true,
        }
    }
}
</script>

<style scoped>
.book-box {
    padding: 15px;
    margin-top: 20px;
    border: 2px solid whitesmoke;
}

</style>