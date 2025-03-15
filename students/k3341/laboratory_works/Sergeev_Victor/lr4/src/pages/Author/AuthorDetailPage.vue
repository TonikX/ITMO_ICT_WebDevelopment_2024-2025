<template>
    <v-app>
    <div class="author-box">
        <v-text-field label="ФИО автора" v-model="author.full_name"></v-text-field>
    </div>
    <v-btn @click="saveAuthor">Сохранить</v-btn>
    </v-app>
</template>
  
  <script>
  import instance from '@/AxiosInstance';
  import { onMounted, ref } from 'vue';
  import { useRoute } from 'vue-router';
  
  export default {
    setup() {
        const author = ref({});
        const id = useRoute().params.id;
  
        const fetchAuthor = async () => {
            try {
                const response = await instance.get('/api/author/' + id);
                author.value = response.data;
            } catch (e) {
                console.log(e)
            }
        }
  
        const saveAuthor = async () => {
            try {
                const response = await instance.patch('/api/author/' + id + '/', author.value);
                if (response.status === 200) {
                    alert('updated successfully');
                }
            } catch (e) {
                console.log(e);
            }
        }
  
        onMounted(fetchAuthor);
  
        return {
            author,
            fetchAuthor,
            saveAuthor,
        }
    },
  };
  </script>
  
  <style scoped>
  .author-box{
    padding: 15px;
    margin-top: 20px;
  }
  </style>