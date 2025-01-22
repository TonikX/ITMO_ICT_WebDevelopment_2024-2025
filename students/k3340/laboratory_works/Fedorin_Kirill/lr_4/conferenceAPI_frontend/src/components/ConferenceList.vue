<template>
    <Base />
    <Participation :show_list="true" ref="create" @update-state="showList"/>
    <h1 v-if="show_list" style="text-align: center;">Конференции</h1>
    <div v-if="show_list" class="conferences__container">
        <div class="conferences__card" v-for="conferences in paginated">
            <div><span style="font-size: large; font-weight: bold;">{{ conferences.name }}</span></div>
            <div><span>Начало: {{ conferences.start_date }}</span></div>
            <div><span>Конец: {{ conferences.end_date }}</span></div>
            <div><span>Осталось мест: {{ conferences.free_places }}</span></div>
            <div>
                <span v-if="!conferences.is_registration_opened || conferences.free_places == 0" style="color: #E40066;">Регистрация закрыта</span>
                <span v-else style="color: green;">Регистрация открыта</span> <br>
                <button v-if="user_conferences.includes(conferences.id)" class="no_participation__button">Вы уже зарегистрированы</button>
                <button v-else-if="!conferences.is_registration_opened || conferences.free_places == 0" class="no_participation__button">Зарегистрироваться</button>
                <button v-else class="participation__button" @click="showParticipation(conferences)">Зарегистрироваться</button>
            </div>
        </div>
    </div>
    <div v-if="show_list" class="pag__btns">
        <label>Страница {{ page+1 }} из {{ max_page+1 }}</label>@
        <button v-if="page==0" disabled @click="prev()">Назад</button>
        <button v-else @click="prev()">Назад</button>
        <button v-if="page==max_page" disabled @click="next()">Вперед</button>
        <button v-else @click="next()">Вперед</button>
    </div>
</template>

<script>
    import axios from "axios";
    import Base from '@/components/Base.vue'
    import Participation from "@/components/Participation.vue";
    
    export default {
        components: {
            Base, Participation
        },
        name: "Conferences",
        data() {
            return {
                all_conferences: [],
                paginated: [],
                page: 0,
                max_page: Number,
                conferences_per_page: 6,
                selected_conferences: "",
                show_list: true,
            }
        },
        methods: {
            showParticipation: function (conferences) {
                const user = JSON.parse(localStorage.getItem('user'));
                if (user) {
                    this.$refs.create.name = conferences.name
                    this.$refs.create.show = true
                    this.$refs.create.participation.conference = conferences.id
                    this.show_list = false
                } else {
                    this.$router.push('/login');
                }
                
            },
            showList() {
                this.$refs.create.show = false
                this.show_list = true
            },
            paginate() {
                let start = this.conferences_per_page * this.page
                let end = Math.min(start + this.conferences_per_page, this.all_conferences.length)
                this.paginated = this.all_conferences.slice(start, end)
            },
            next() {
                this.page++
                this.paginate()
            },
            prev() {
                if (this.page > 0)
                    this.page--
                this.paginate()
            },
            async fetchConferenceList () {
                try {
                    const response = await axios.get('http://127.0.0.1:8000/conferences/list/');
                    const user = JSON.parse(localStorage.getItem('user'));
                    const second_response = await axios.get(`http://127.0.0.1:8000/users/${user.id}/conferences/`);
                    this.user_conferences = second_response.data.map(conference => conference.id)
                    this.all_conferences = response.data
                    this.max_page =  Math.round(this.all_conferences.length / this.conferences_per_page)
                    this.paginate()
                } catch (e) {
                    if (e.response) {
                        switch (e.response.status) {
                            case 404:
                                break;
                            default:
                                alert('Ошибка ответа!');
                        } 
                    } else if (e.request) {
                        alert('Ошибка запроса!');
                    }
                }
            }
        },
        mounted() {
            this.fetchConferenceList() 
        }
    }
</script>

<style>
    .conferences__container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        justify-content: center;
        max-width: 80%;
        margin: auto;
        column-gap: 1em;    
        row-gap: 1em;
    }

    .conferences__card {
        background-color: #fff;
        border-radius: 10px;
        padding: 10%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        max-width: 100%;
        transition: transform 0.3s;
    }

    .conferences__card div {
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .conferences__card:hover {
        transform: translateY(-5px);
    }

    .participation__button {
        background-color: #1C7C54;
        color: white;
        border: none;
        margin-top: 10px;
        padding: 10px 15px;
        width: 100%;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .no_participation__button {
        background-color: #A0A0A0;
        color: white;
        border: none;
        margin-top: 10px;
        padding: 10px 15px;
        width: 100%;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .pag__btns {
        margin-top: 5%;
        display: flex;
        gap: 10px;
        justify-content: center;
    }
</style>