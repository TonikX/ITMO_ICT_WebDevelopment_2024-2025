<template>
<v-app>
    <v-banner><h1>Читальные залы</h1></v-banner>
    <v-btn @click="$router.push('/room/create')">Добавить зал</v-btn>
    <v-btn @click="fetchRooms">Загрузить читальные залы</v-btn>
    <div v-if="!isLoading">
        <transition-group name="reading-room-list">
            <reading-room-list
            :rooms="rooms"
            @remove_room="deleteRoom"
            />
        </transition-group>
    </div>
    <div v-else>
        Идёт загрузка
    </div>
</v-app>
</template>

<script>
import { onMounted, ref } from 'vue';
import ReadingRoomList from '@/components/ReadingRoom/ReadingRoomList.vue';
import instance from '@/AxiosInstance';
export default {
    components: {ReadingRoomList},
    setup() {
        const rooms = ref([]);
        const isLoading = ref(false);

        const fetchRooms = async () => {
            isLoading.value = true;
            try {
                const response = await instance.get('/api/room');
                rooms.value = response.data;
            } catch(e) {
                console.log(e);
            } finally {
                isLoading.value = false;
            }
        }

        const deleteRoom = async (id) => {
            try {
                const response = await instance.delete('/api/room/' + id + '/');
                if (response.status === 204) {
                    fetchRooms();
                }
            } catch (e) {
                console.log(e)
            }
        }

        onMounted(fetchRooms);

        return {
            rooms,
            isLoading,
            fetchRooms,
            deleteRoom,
        }
    },
};
</script>

<style scoped>
</style>