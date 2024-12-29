<template>
    <div v-if="genres.length > 0">
        <transition-group name="genre-items">
            <genre-list-item v-for="genre in genres"
            :genre="genre"
            :key="genre.id"
            @remove_genre="$emit('remove_genre', genre.id)"
            />
        </transition-group>
    </div>
    <div v-else style="color: red">
        Жанров нет
    </div>
</template>

<script>
import GenreListItem from './GenreListItem.vue';
export default {
    components: {GenreListItem},
    props: {
        genres: {
            type: Array,
            required: true,
        }
    }
};
</script>

<style scoped>

</style>