<template>
    <div v-if="show" class="participation__form__container">
        <h2>Регистрация на  {{ name }}</h2>
        <label v-if="this.error_message" style="color: red;">{{ this.error_message }}</label>
        <form @submit.prevent="createParticipation">
            <div class="form__group">
                <label for="participation.from_town">Укажите ваш город</label>
                <input type="text" id="__username" v-model="participation.from_town" required />
            </div>
            <div class="form__group">
                <label for="participation.publication_theme">Тема вашего доклада</label>
                <input type="text_area" id="__username" v-model="participation.publication_theme" required />
            </div>
            <button type="submit" class="submit__button">Зарегистрироваться</button>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Participation',
        data() {
            return {
                participation: {
                    conference: '',
                    client: '',
                    registration_date: '',
                    publication_theme: '',
                    from_town: '',
                },
                show: false,
                name: "",
                error_message: "",
            }
        },
        props : [
            'show_list'
        ],
        methods: {
            hideParticipation () {
                this.$emit('update-state', true)
            },
            async createParticipation () {
                try {
                    this.participation.client = JSON.parse(localStorage.getItem('user')).id;
                    this.participation.registration_date = new Date().toJSON().slice(0, 10);
                    console.log(this.participation)
                    await axios.post('http://127.0.0.1:8000/participation/add/', this.participation);
                    this.$router.push('/participation');
                } catch (e) {
                    if (e.response) {
                        switch (e.response.status) {
                            case 401:
                                break;
                            case 400:
                                console.log(e.response.data)
                                this.error_message = e.response.data["message"]
                            default:
                        }
                    }
                }
            }
        }
    }
</script>

<style>
    @import '../assets/participation.css';
</style>