<template>
    <div class="book-copy-box">
        <div class="book-copy-title">
            <h3>{{ book_copy.book.title }}</h3>
        </div>
        <div class="book-copy-publisher">
            Шифр: <router-link
            :to="{path: `/book_copy/${book_copy.id}`}">
                {{ book_copy.cipher }}
            </router-link>
        </div>
        <br>
        <button @click="$emit('remove_copy', book_copy)" style="color: red;">Удалить</button>
    </div>
</template>

<script>
export default {
    props: {
        book_copy: {
            type: Object,
            required: true,
        }
    }
}
</script>

<style scoped>
.book-copy-box {
    padding: 15px;
    margin-top: 20px;
    border: 2px solid whitesmoke;
}

</style>