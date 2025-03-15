<template>
<v-app>
    <div class="reading-room-box">
        <v-text-field label="Название зала" v-model="room.name"></v-text-field>
        <v-text-field label="Вместимость" v-model="room.capacity"></v-text-field>
        <v-btn @click="saveRoom">Сохранить</v-btn>
    </div>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
    setup() {
        const room = ref({});
        const id = useRoute().params.id;

        const fetchRoom = async () => {
            try {
                const response = await instance.get('/api/room/' + id );
                room.value = response.data;
            } catch (e) {
                console.log(e);
            }
        };

        const saveRoom = async () => {
            try {
                const response = await instance.patch('/api/room/' + id + '/', room.value);
                if (response.status === 200) {
                    alert('updated successfully');
                }
            } catch (e) {
                console.log(e);
            }
        }

        onMounted(fetchRoom);

        return {
            room,
            fetchRoom,
            saveRoom,
        }
    },
};
</script>

<style scoped>
.reading-room-box {
    padding: 15px;
    margin-top: 20px;
}

</style>