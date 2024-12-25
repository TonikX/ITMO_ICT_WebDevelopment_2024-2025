<template>
    <div class="container col-md-8">
        <h1>Edit data</h1>
        <user-form :mode="'edit'" :initialData=initialData></user-form>
    </div>
</template>

<script>
import UserForm from '@/components/UserForm.vue';
import axios from 'axios'

export default {
    components: {
        UserForm
    },
    data() {
        return {
            initialData: {},
        }
    },
    mounted() {
        this.fetchData()
    },
    methods: {
        async fetchData() {
            try {
        const token = localStorage.getItem('token');

        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };

        const response = await axios.get(' http://127.0.0.1:8000/auth/users/me/', config);
        this.initialData = response.data;
      } catch (error) {
        console.error(error);
      }
        }
    }
    
}
</script>

<style>
.container {
    margin: 10px;
}
</style>