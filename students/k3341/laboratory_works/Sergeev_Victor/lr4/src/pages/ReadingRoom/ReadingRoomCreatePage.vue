<template>
<v-app>
    <div class="reading-room-create-room">
        <v-form @submit.prevent="createRoom">
            <v-text-field label="Название зала" v-model="room.name"></v-text-field>
            <v-text-field label="Вместимость" v-model="room.capacity"></v-text-field>
            <v-btn type="submit">Создать читальный зал</v-btn>
        </v-form>
    </div>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import router from '@/router';
import { ref } from 'vue';
export default {
    setup() {
        const room = ref({});

        const createRoom = async () => {
            try {
                const response = await instance.post('/api/room/create/', room.value);
                if (response.status === 201) {
                    router.push('/room');
                }
            } catch (e) {
                console.log(e);
            }
        }

        return {
            room,
            createRoom,
        };
    },
};
</script>

<style scoped>
</style>