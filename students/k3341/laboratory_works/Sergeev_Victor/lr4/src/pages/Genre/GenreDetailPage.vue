<template>
<v-app>
    <div>
    <v-text-field label="Название" v-model="genre.title"></v-text-field>
    </div>
    <v-btn @click="saveGenre">Сохранить</v-btn>
</v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
    setup() {
        const genre = ref({});
        const id = useRoute().params.id;

        const fetchGenre = async () => {
            try {
                const response = await instance.get('/api/genre/' + id);
                genre.value = response.data;
            } catch (e) {
                console.log(e)
            }
        }

        const saveGenre = async () => {
            try {
                const response = await instance.patch('/api/genre/' + id + '/', genre.value);
                if (response.status === 200) {
                    alert('updated successfully');
                }
            } catch (e) {
                console.log(e);
            }
        }

        onMounted(fetchGenre);

        return {
            genre,
            fetchGenre,
            saveGenre,
        }
    },
};
</script>

<style scoped>
 .genre-box{
    padding: 15px;
    margin-top: 20px;
 }
</style>