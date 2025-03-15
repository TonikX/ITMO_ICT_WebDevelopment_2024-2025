<template>
    <div v-if="rooms.length > 0">
        <transition-group name="reading-room-list">
            <reading-room-list-item v-for="room in rooms"
            :room="room"
            :key="room.id"
            @remove_room="$emit('remove_room', room.id)"
            />
        </transition-group>
    </div>
    <div v-else style="color: red">
        Нет залов
    </div>
</template>

<script>
import ReadingRoomListItem from './ReadingRoomListItem.vue';
export default{
    components: {ReadingRoomListItem},
    props: {
        rooms: {
            type: Array,
            required: true,
        }
    }
}
</script>

<style scoped>

</style>