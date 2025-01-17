<template>
  <div>
    <h2>Список сотрудников</h2>
    <table>
      <thead>
        <tr>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Должность</th>
          <th>Email</th>
          <th>Телефон</th>
          <th>Типография</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="employee in employees" :key="employee.id">
          <td>{{ employee.first_name }}</td>
          <td>{{ employee.last_name }}</td>
          <td>{{ employee.position }}</td>
          <td>{{ employee.email }}</td>
          <td>{{ employee.phone_number }}</td>
          <td>{{ employee.printshop_name }}</td>
          <td>
            <button @click="$emit('edit', employee)">Редактировать</button>
            <button @click="$emit('delete', employee.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    employees: { type: Array, required: true },
  },
};
</script>
