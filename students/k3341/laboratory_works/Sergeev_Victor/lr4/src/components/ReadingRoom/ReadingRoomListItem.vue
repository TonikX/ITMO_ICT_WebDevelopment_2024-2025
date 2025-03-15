<template>
    <div class="reading-room-box">
        <div class="reading-room-name">
            <router-link
            :to="{path: `/room/${room.id}`}">
                {{ room.name }}
            </router-link>
        </div>
        <div class="reading-room-max-capacity">
            Вместимость: {{ room.capacity }}
        </div>
        <br>
        <button class="delete-button"
        @click="$emit('remove_room', room)"
        style="color: red;">
            Удалить
        </button>
    </div>
</template>

<script>
export default {
    props: {
        room: {
            type: Object,
            required: true,
        }
    }
}
</script>

<style scoped>
.reading-room-box {
    padding: 15px;
    margin-top: 20px;
    border: 2px solid whitesmoke;
}

</style>