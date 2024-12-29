<template>
    <div v-if="authors.length > 0">
        <transition-group name="author-list">
            <author-list-item v-for="author in authors"
            :author="author"
            :key="author.id"
            @remove_author="$emit('remove_author', author.id)"
            />
        </transition-group>
    </div>
    <div v-else style="color: red">
        Авторов нет
    </div>
</template>

<script>
import AuthorListItem from './AuthorListItem.vue';
export default {
    components: {AuthorListItem},
    props: {
        authors: {
            type: Array,
            required: true,
        }
    },
};
</script>

<style scoped>

</style>