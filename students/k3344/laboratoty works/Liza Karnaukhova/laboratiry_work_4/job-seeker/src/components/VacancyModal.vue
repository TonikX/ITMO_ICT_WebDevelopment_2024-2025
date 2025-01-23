<template>
  <div class="modal fade show" tabindex="-1" style="display: block;" aria-modal="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Добавить новую вакансию</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitVacancy">
            <div class="form-group mb-3">
              <label for="vacanciesTitle">Название вакансии</label>
              <input type="text" class="form-control" v-model="vacancy.title" placeholder="Введите название вакансии" required />
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesCompany">Компания</label>
              <input type="text" class="form-control" v-model="vacancy.company" placeholder="Введите название компании" required />
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesSalary">Зарплата</label>
              <input type="number" class="form-control" v-model="vacancy.salary" placeholder="Введите зарплату" required />
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesExperience">Требуемый опыт работы</label>
              <input type="text" class="form-control" v-model="vacancy.experience" placeholder="Введите опыт работы" required />
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesAddress">Адрес</label>
              <input type="text" class="form-control" v-model="vacancy.address" placeholder="Введите адрес" required />
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesDescription">Описание вакансии</label>
              <textarea class="form-control" v-model="vacancy.description" placeholder="Введите описание вакансии" required></textarea>
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesResponsibilities">Обязанности</label>
              <textarea class="form-control" v-model="vacancy.responsibility" placeholder="Введите обязанности" required></textarea>
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesRequirements">Требования</label>
              <textarea class="form-control" v-model="vacancy.requirements" placeholder="Введите требования" required></textarea>
            </div>
            <div class="form-group mb-3">
              <label for="vacanciesConditions">Условия</label>
              <textarea class="form-control" v-model="vacancy.conditions" placeholder="Введите условия" required></textarea>
            </div>
            <button type="submit" class="btn btn-custom-primary">Добавить вакансию</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue';

  export default {
    setup(props, { emit }) { // Добавляем emit как второй аргумент
      const vacancy = ref({
        title: '',
        company: '',
        salary: null,
        experience: '',
        address: '',
        description: '',
        responsibility: '',
        requirements: '',
        conditions: '',
      });

      const submitVacancy = () => {
        // Emit the vacancy data to the parent component
        emit('submit', { ...vacancy.value }); // Используем emit вместо this.$emit
        // Reset the form
        vacancy.value = {
          title: '',
          company: '',
          salary: null,
          experience: '',
          address: '',
          description: '',
          responsibility: '',
          requirements: '',
          conditions: '',
        };
      };

      return {
        vacancy,
        submitVacancy,
      };
    },
  };
</script>

<style scoped>
  /* Добавьте стили, если необходимо */
</style>
