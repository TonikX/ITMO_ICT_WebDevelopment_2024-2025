<template>
    <v-app>
    <v-banner><h1>Авторы</h1></v-banner>
    <v-btn @click="$router.push('/author/create')">Добавить автора</v-btn>
    <br>    
    <v-btn @click="fetchAuthors">Загрузить авторов</v-btn>
    <div v-if="!isLoading">
    <transition-group name="author-list">
        <author-list
        :authors="authors" 
        @remove_author="deleteAuthor"/>
    </transition-group>
    </div>
    <div v-else>
        Идёт загрузка
    </div>
    </v-app>
</template>

<script>
import instance from '@/AxiosInstance';
import AuthorList from '@/components/Author/AuthorList.vue';
import { onMounted, ref } from 'vue';
export default {
    components: {AuthorList},
    setup() {
        const authors = ref([]);
        const isLoading = ref(false);

        const fetchAuthors = async () => {
            isLoading.value = true
            try {
                const response = await instance.get('/api/author')
                authors.value = response.data;
            } catch(e) {
                console.log(e);
            } finally {
                isLoading.value = false;
            }
        };

        const deleteAuthor = async (id) => {
            try {
                const response = await instance.delete('/api/author/' + id + '/');
                if (response.status === 204) {
                    fetchAuthors();
                } 
            } catch (e) {
                console.log(e);
            }
        };

        onMounted(fetchAuthors);

        return {
            authors,
            isLoading,
            fetchAuthors,
            deleteAuthor,
        };
    },
};
</script>

<style scoped>
</style>