<template>
  <div class="col-12">
    <h5>Ваше резюме</h5>
  </div>
  <div class="col-12">
    <div class="table-responsive">
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Должность</th>
            <th>Имя</th>
            <th>Фамилия</th>
            <th>Телефон</th>
            <th>Email</th>
            <th>Опыт работы</th>
            <th>Образование</th>
            <th>Навыки</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="resume in resumes" :key="resume.id">
            <td>{{ resume.title }}</td>
            <td>{{ resume.name }}</td>
            <td>{{ resume.last_name }}</td>
            <td>{{ resume.number }}</td>
            <td>{{ resume.email }}</td>
            <td>{{ resume.experience }}</td>
            <td>{{ resume.education }}</td>
            <td>{{ resume.skills }}</td>
            <td>
              <button class="btn button btn-custom" @click="$emit('delete-resume', resume.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="col-12">
    <button type="button" class="btn button btn-custom" @click="$emit('add-resume')">Добавить резюме</button>
  </div>
</template>

<script>
  export default {
    props: {
      resumes: {
        type: Array,
        required: true
      }
    }
  };
</script>

<style scoped>
  /* Добавьте стили, если необходимо */
</style>
