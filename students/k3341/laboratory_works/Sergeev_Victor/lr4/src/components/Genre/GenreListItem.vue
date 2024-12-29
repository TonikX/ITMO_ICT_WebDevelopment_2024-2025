<template>
    <div class="genre-box">
        <div class="genre-title">
            <router-link :to="{path: `/genre/${genre.id}`}">{{ genre.title }}</router-link>
        </div>
        <br>
        <button class="delete-button" @click="$emit('remove_genre', genre)" style="color: red;">
            Удалить
        </button>
    </div>
</template>

<script>
export default {
    props: {
        genre: {
            type: Object,
            required: true,
        }
    }
}
</script>

<style scoped>
 .genre-box{
    padding: 15px;
    margin-top: 20px;
    border: 1px solid whitesmoke;
 }
</style>