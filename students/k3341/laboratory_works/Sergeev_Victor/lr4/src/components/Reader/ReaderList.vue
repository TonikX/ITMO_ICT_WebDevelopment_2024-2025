<template>
    <div v-if="readers.length > 0">
        <transition-group name="reader-list">
            <reader-list-item v-for="reader in readers"
            :reader="reader"
            :key="reader.id"
            @remove_reader="$emit('remove_reader', reader.id)"
            />
        </transition-group>
    </div>
    <div v-else style="color: red">
        Нет читателей
    </div>
</template>

<script>
import ReaderListItem from './ReaderListItem.vue';
export default {
    components: {ReaderListItem},
    props: {
        readers: {
            type: Array,
            required: true,
        }
    }
}
</script>

<style scoped>

</style>