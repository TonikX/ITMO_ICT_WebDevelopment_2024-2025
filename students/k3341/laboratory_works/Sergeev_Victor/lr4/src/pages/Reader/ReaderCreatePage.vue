<template>
<v-app>
    <div class="reader-create-form">
        <v-form @submit.prevent="createReader">
            <v-text-field label="ФИО читателя" v-model="reader.full_name"></v-text-field>
            <v-text-field label="Номер паспорта" v-model="reader.passport_number"></v-text-field>
            <v-text-field label="День рождения" v-model="reader.birthdate"></v-text-field>
            <v-text-field label="Адрес" v-model="reader.address"></v-text-field>
            <v-text-field label="Телефон" v-model="reader.phone_number"></v-text-field>
            <v-select label="Образование"
                v-model="reader.education"
                :items="educationItems"
                item-title="label"
                item-value="value"/>
            <v-text-field label="Номер читательского билета" v-model="reader.reading_ticket_number"></v-text-field>
            <v-text-field label="ID читального зала" v-model="reader.reading_room"></v-text-field>
            <v-btn type="submit">Создать читателя</v-btn>
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
        const reader = ref({
            id: '',
            full_name: '',
            passport_number: '',
            birthdate: '',
            address: '',
            phone_number: '',
            education: 'н',
            degree: false,
            reading_ticket_number: '',
            reading_room: '',
        })
        const educationItems = [
            { value: 'н', label: 'Начальное' },
            { value: 'с', label: 'Среднее' },
            { value: 'в', label: 'Высшее' },
        ]

        const createReader = async () => {
            try {
                console.log(reader.value)
                const response = await instance.post('/api/reader/create/', reader.value);
                if (response.status === 201) {
                    router.push('/reader')
                }
            } catch(e) {
                console.log(e.response)
            };
        }

        return {
            reader,
            educationItems,
            createReader,
        }
    },
};
</script>

<style scoped>

</style>