<template>
    <div class="book-take-box">
        <div class="book-take-id">
            ID: <router-link
            :to="{path: `/book_take/${book_take.id}`}">{{ book_take.id }}</router-link>
        </div>
        <div class="book-take-reader">
            Читатель: {{ book_take.reader.id }}
        </div>
        <div class="book-take-book-copy">
            Копия книги: {{ book_take.book_copy.id }}
        </div>
        <div class="book-take-take-date">
            Дата взятия: {{ book_take.take_date }}
        </div>
        <div v-if="book_take.restore_date" class="book-take-restore-date">
            Дата возврата: {{ book_take.restore_date }}
        </div>
    </div>
</template>

<script>
export default {
    props: {
        book_take: {
            type: Object,
            required: true,
        }
    }
}
</script>

<style scoped>
 .book-take-box{
    padding: 15px;
    margin-top: 20px;
    border: 2px solid whitesmoke;
 }
</style>