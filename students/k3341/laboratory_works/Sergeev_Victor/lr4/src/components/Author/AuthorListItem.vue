<template>
    <div class="author-box">
        <div class="author-full-name">
            <router-link
            :to="{path: `/author/${author.id}`}">
            {{ author.full_name }}
        </router-link>
        </div>
        <br>
        <button class="delete-button" @click="$emit('remove_author', author)" style="color: red;">
            Удалить
        </button>
    </div>
</template>

<script>
export default {
    props: {
        author: {
            type: Object,
            required: true,
        }
    }
}
</script>

<style scoped>
 .author-box{
    padding: 15px;
    margin-top: 20px;
    border: 1px solid whitesmoke;
 }
</style>