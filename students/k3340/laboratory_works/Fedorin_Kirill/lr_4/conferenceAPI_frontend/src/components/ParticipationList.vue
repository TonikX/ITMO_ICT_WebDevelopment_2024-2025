<template>
    <Base/>
    <DeleteParticipation ref="del"/>
    <UpdateParticipation ref="upt"/>
    <div v-if="this.user" class="participation__history__container">
    <h1>Участие</h1>
    <table class="participation__table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Конференция</th>
                <th>Дата регистрации</th>
                <th>Тема доклада</th>
                <th>Действия</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="participation in participations" :key="participation.id">
                <td>{{ participation.id }}</td>
                <td>{{ participation.conference }}</td>
                <td>{{ participation.registration_date }}</td>
                <td>{{ participation.from_town }}</td>
                <td v-if="participation.from_town != 'finished'">
                    <a class="action__button delete__button" @click="showModalDelete(participation.id)">удалить</a> 
                    <a class="action__button edit__button" @click="showModalUpdate(participation.id)">редактировать</a> 
                </td>
                <td v-if="participation.from_town == 'finished'"> нельзя внести изменения </td>
            </tr>
        </tbody>
    </table>
    </div>
</template>

<script>
    import Base from '@/components/Base.vue';
    import DeleteParticipation from '@/components/DeleteParticipation.vue';
    import UpdateParticipation from '@/components/UpdateParticipation.vue';
    import axios from 'axios';

    export default {
        name: 'ParticipationList',
        components: {
            Base, DeleteParticipation, UpdateParticipation
        },
        data() {
            return {
                participations: [],
                user: {}
            }
        },
        methods: {
            showModalDelete: function (id) {
                this.$refs.del.show = true
                this.$refs.del.participationId = id
            },
            showModalUpdate: function (id) {
                this.$refs.upt.show = true
                this.$refs.upt.participationId = id
            },
            async fetchUserParticipation() {
                this.user = JSON.parse(localStorage.getItem('user'));
                try {
                    const response = await axios.get(`http://127.0.0.1:8000/users/${this.user.id}/participation`);
                    this.participations = response.data;
                    console.log(this.participations);
                    this.participations.forEach(async (participation) => {
                        const conference_resp = await axios.get(`http://127.0.0.1:8000/conferences/${participation.conference}/`);
                        participation.conference = conference_resp.data.name;
                    });
                } catch (e) {
                    if (e.response) {
                        switch (e.response.status) {
                            case 401:
                                this.user = {};
                                break;
                            default:
                        }
                    }
                }
            }
        }, 
        mounted() {
            this.fetchUserParticipation()
        }
    }
</script>

<style>
    .participation__history__container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f9f9f9;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    h1 {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .participation__table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1.5rem;
    }

    .participation__table th, .participation__table td {
        padding: 0.75rem;
        text-align: left;
        border: 1px solid #ddd;
    }

    .participation__table th {
        background-color: #007bff;
        color: white;
    }

    .participation__table tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    .participation__table tr:hover {
        background-color: #ddd;
    }

    .participation__table td {
        font-size: 0.9rem;
    }

    .action__button {
        padding: 8px 12px;
        margin-right: 5px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 0.3s ease;
    }

    .edit__button {
        background-color: #3498db;
        color: white;
    }

    .edit__button:hover {
        background-color: #2980b9; 
    }

    .delete__button {
        background-color: #e74c3c;
        color: white;
    }

    .delete__button:hover {
        background-color: #c0392b; 
    }
</style>