<template>
    <div v-if="show" class="modal__shadow" @click.self="closeModal">
        <div class="modal">
            <div class="modal__close" @click="closeModal">&#10006;</div>
                <h2>Редактирование участия</h2>
                <label v-if="this.error_msg" style="color: red;">{{ this.error_msg }}</label>
                <form @submit.prevent="updateParticipation">
                    <div class="form__group">
                        <label for="publication_theme">Тема доклада</label>
                        <input type="text" id="__username" v-model="publication_theme" required />
                    </div>
                    <div class="form__group">
                        <label for="from_town">Ваш город</label>
                        <input type="text" id="__checkInDate" v-model="from_town" required />
                    </div>
                    <button type="submit" class="submit__button">Редактировать</button>
                </form>
        </div> 
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'UpdateParticipation',
        data() {
            return {
                publication_theme: '',
                from_town: '',
                show: false,
                participationId: Number,
                error_msg: '',
            }
        },
        methods: {
            closeModal () {
                this.show = false
            },
            async updateParticipation () {
                try {
                    console.log(axios.defaults.headers.common['Authorization']);
                    const response = await axios.patch(`http://127.0.0.1:8000/participation/${this.participationId}/update/`, {
                        publication_theme: this.publication_theme,
                        from_town: this.from_town,
                    });
                    this.closeModal();
                    window.location.reload();
                } catch (e) {
                    if (e.response) {
                        switch (e.response.status) {
                            case 401:
                                break;
                            case 400:
                                this.error_msg = e.response.data['message']
                            default:
                        }
                    }
                }
            }
        } 
    }
</script>

<style>
    @import '../assets/modal.scss';
    @import '../assets/participation.css';
</style>