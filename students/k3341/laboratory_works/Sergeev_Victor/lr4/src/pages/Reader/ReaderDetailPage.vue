<template>
<v-app>
    <div v-if="reader.full_name" class="reader-box">
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
        <v-btn @click="saveReader">Сохранить</v-btn>
        <v-btn @click="$router.push(`/reader/book_take/${reader.id}`)">Взятые книги</v-btn>
    </div>
    <div v-else>
        Нет такого читателя
    </div>
</v-app>
</template>

<script>
import ReadingRoomListItem from '@/components/ReadingRoom/ReadingRoomListItem.vue';
import { onMounted, ref } from 'vue';
import instance from '@/AxiosInstance';
import { useRoute } from 'vue-router';
export default {
    components: {ReadingRoomListItem},
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
        const id = useRoute().params.id;

        const fetchReader = async () => {
            try {
                const response = await instance.get('/api/reader/' + id);
                reader.value = response.data;
            } catch (e) {
                console.log(e);
            }
        };

        const saveReader = async () => {
            try {
                const response = await instance.patch('/api/reader/' + id + '/', reader.value);
                console.log(response.data)
                if (response.status === 200) {
                    alert('updated successfully');
                }
            } catch (e) {
                console.log(e);
            }
        }

        onMounted(fetchReader);

        return {
            reader,
            educationItems,
            fetchReader,
            saveReader,
        }
    },
};
</script>

<style scoped>
.book-box {
    padding: 15px;
    margin-top: 20px;
}

</style>