<template>
  <div>
    <h5>Отклики на вакансии</h5>
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th>Кандидат</th>
          <th>Email</th>
          <th>Опыт</th>
          <th>Образование</th>
          <th>Навыки</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="response in responses" :key="response.id">
          <td>{{ response.full_name }}</td>
          <td>{{ response.email }}</td>
          <td>{{ response.experience }}</td>
          <td>{{ response.education }}</td>
          <td>{{ response.skills }}</td>
          <td>
            <button @click="deleteResponse(response.id)" class="btn button btn-custom">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { onMounted } from 'vue';
  import { useResponsesStore } from '@/stores/responses';

  export default {
    props: {
      responses: Array
    },
    setup() {
      const responsesStore = useResponsesStore();

      // Загружаем отклики с резюме
      onMounted(() => {
        responsesStore.getAllResponsesWithResumes();
      });

      const deleteResponse = async (responseId) => {
        await responsesStore.deleteResponse(responseId);
      };

      return { deleteResponse, responses: responsesStore.responses };
    }
  };

</script>

