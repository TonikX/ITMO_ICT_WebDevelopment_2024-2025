<template>
<v-app>
    <v-banner><h1>Читатели</h1></v-banner>
    <v-btn @click="$router.push('/reader/create')">Добавить читателя</v-btn>
    <br>
    <br>
    <v-btn @click="fetchReaders('all')">Загрузить читателей</v-btn>
    <v-btn @click="fetchReaders('young')">Загрузить молодных читателй</v-btn>
    <v-btn @click="fetchReaders('delay_month')">Не сдавшие книгу спустя месяц</v-btn>
    <v-btn @click="fetchReaders('less')">Взявшие книгу, которых не более 5 в библиотеке</v-btn>
    <div v-if="!isLoading">
        <transition-group name="reader-list">
            <reader-list
            :readers="readers"
            @remove_reader="deleteReader"
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
import ReaderList from '@/components/Reader/ReaderList.vue';
import instance from '@/AxiosInstance';
export default {
    components: {ReaderList},
    setup() {
        const readers = ref([]);
        const isLoading = ref(false);
        const urls = new Map([
            ['all', '/api/reader'],
            ['young', '/api/reader/age/young'],
            ['delay_month', '/api/reader/delay/month'],
            ['less', '/api/reader/less/5'],
        ])

        const fetchReaders = async (url_key) => {
            isLoading.value = true;
            const url = urls.get(url_key)
            try {
                const response = await instance.get(url)
                readers.value = response.data;
            } catch(e) {
                console.log(e);
            } finally {
                isLoading.value = false;
            }
            console.log(readers.value);
            console.log(url);
        };

        const deleteReader = async (id) => {
            try {
                const response = await instance.delete('/api/reader/' + id + '/');
                if (response.status === 204) {
                    fetchReaders();
                }
            } catch (e) {
                console.log(e);
            }
        }

        onMounted(() => fetchReaders('all'))

        return {
            readers,
            isLoading,
            fetchReaders,
            deleteReader,
        };
    },
};
</script>

<style scoped>

</style>