<template>
  <div class="modal fade show" tabindex="-1" style="display: block;" aria-modal="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Добавить резюме</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitResume">
            <div class="form-group mb-3">
              <label for="resumeTitle">Должность</label>
              <input type="text" class="form-control" v-model="resume.title" placeholder="Введите вашу должность" required>
            </div>
            <div class="form-group mb-3">
              <label for="resumeName">Имя</label>
              <input type="text" class="form-control" v-model="resume.name" placeholder="Введите ваше имя" required>
            </div>
            <div class="form-group mb-3">
              <label for="resumeSurname">Фамилия</label>
              <input type="text" class="form-control" v-model="resume.last_name" placeholder="Введите вашу фамилию" required>
            </div>
            <div class="form-group mb-3">
              <label for="resumePhone">Телефон</label>
              <input type="text" class="form-control" v-model="resume.number" placeholder="Введите ваш телефон" required>
            </div>
            <div class="form-group mb-3">
              <label for="resumeEmail">Email</label>
              <input type="email" class="form-control" v-model="resume.email" placeholder="Введите ваш email" required>
            </div>
            <div class="form-group mb-3">
              <label for="resumeExperience">Опыт работы</label>
              <input type="text" class="form-control" v-model="resume.experience" placeholder="Введите ваш опыт работы" required>
            </div>
            <div class="form-group mb-3">
              <label for="resumeEducation">Образование</label>
              <input type="text" class="form-control" v-model="resume.education" placeholder="Введите ваше образование" required>
            </div>
            <div class="form-group mb-3">
              <label for="resumeSkills">Навыки</label>
              <input type="text" class="form-control" v-model="resume.skills" placeholder="Введите ваши навыки" required>
            </div>
            <button type="submit" class="btn btn-custom-primary">Добавить резюме</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue';

  export default {
    setup(props, { emit }) {
      const resume = ref({
        title: '',
        name: '',
        last_name: '',
        number: '',
        email: '',
        experience: '',
        education: '',
        skills: '',
      });

      const submitResume = () => {
        // Emit the resume data to the parent component
        emit('submit', { ...resume.value });
        // Reset the form
        resume.value = {
          title: '',
          name: '',
          last_name: '',
          number: '',
          email: '',
          experience: '',
          education: '',
          skills: '',
        };
      };

      return {
        resume,
        submitResume,
      };
    },
  };
</script>

<style scoped>
  /*
  /* Добавьте стили, если необходимо */
</style>
