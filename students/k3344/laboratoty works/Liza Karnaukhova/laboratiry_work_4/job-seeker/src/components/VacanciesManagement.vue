<template>
  <div class="col-12">
    <h5>Управление вакансиями</h5>
  </div>
  <div class="col-12 mb-2">
    <button @click="$emit('add-vacancy')" class="btn btn-custom">Добавить новую вакансию</button>
  </div>
  <div class="col-12">
    <div class="table-responsive">
      <table id="vacancies-table" class="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Название</th>
            <th>Компания</th>
            <th>Зарплата</th>
            <th>Опыт</th>
            <th>Адрес</th>
            <th>Описание</th>
            <th>Обязанности</th>
            <th>Требования</th>
            <th>Условия</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody id="vacancies-table-body">
          <tr v-for="vacancy in vacancies" :key="vacancy.id">
            <td>{{ vacancy.title }}</td>
            <td>{{ vacancy.company }}</td>
            <td>{{ vacancy.salary }}</td>
            <td>{{ vacancy.experience }}</td>
            <td>{{ vacancy.address }}</td>
            <td>{{ vacancy.description }}</td>
            <td>
              <div v-if="Array.isArray(vacancy.responsibility)">
                <div v-for="(item, index) in vacancy.responsibility" :key="index">{{ item }}<br></div>
              </div>
              <div v-else>{{ vacancy.responsibility }}</div>
            </td>
            <td>
              <div v-if="Array.isArray(vacancy.requirements)">
                <div v-for="(item, index) in vacancy.requirements" :key="index">{{ item }}<br></div>
              </div>
              <div v-else>{{ vacancy.requirements }}</div>
            </td>
            <td>
              <div v-if="Array.isArray(vacancy.conditions)">
                <div v-for="(item, index) in vacancy.conditions" :key="index">{{ item }}<br></div>
              </div>
              <div v-else>{{ vacancy.conditions }}</div>
            </td>
            <td>
              <button @click="deleteVacancy(vacancy.id)" class="btn button btn-custom">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
  import { useVacanciesStore } from '@/stores/vacancies1';

  export default {
  props: {
    vacancies: Array,
  },
  emits: ['add-vacancy'], // Указываем событие
  setup() {
    const vacanciesStore = useVacanciesStore();

    const deleteVacancy = async (vacancyId) => {
      await vacanciesStore.deleteVacancy(vacancyId);
    };

    return { deleteVacancy };
  },
};

</script>
