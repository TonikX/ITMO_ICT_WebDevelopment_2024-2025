<template>
    <v-app>
    <div class="author-create-form">
        <v-form @submit.prevent="createAuthor">
            <v-text-field label="ФИО автора" v-model="author.full_name"></v-text-field>
            <v-btn type="submit">Создать автора</v-btn>
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
        const author = ref({
            full_name: ''
        })

        const createAuthor = async () => {
            try {
                const response = await instance.post('/api/author/create/', author.value);
                if (response.status === 201) {
                    router.push('/author')
                }
            } catch(e) {
                console.log(e)
            };
        }

        return {
            author,
            createAuthor,
        }
    },
};
</script>

<style scoped>

</style>