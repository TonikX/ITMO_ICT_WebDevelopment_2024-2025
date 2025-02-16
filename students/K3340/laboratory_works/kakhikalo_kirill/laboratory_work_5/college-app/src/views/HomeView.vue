<template>
  <div>
    <h2>Как пользоваться системой</h2>
    <ul>
      <li>
        <strong>Какой предмет будет в заданной группе в заданный день недели на заданном уроке?</strong><br />
        Узнайте расписание, выбрав нужную группу и день недели (например, в разделе
        <router-link to="/schedule">Расписание</router-link>).
      </li>
      <li>
        <strong>Кто из преподавателей преподает в заданной группе?</strong><br />
        Можно посмотреть список преподавателей по группе (например, в разделе
        <router-link to="/teachers">Преподаватели</router-link>) или через поиск по расписанию.
      </li>
      <li>
        <strong>В каких группах преподает заданный предмет заданный преподаватель?</strong><br />
        Узнайте все дисциплины преподавателя и сопоставьте их с группами (см. раздел 
        <router-link to="/disciplines">Дисциплины</router-link> и 
        <router-link to="/teachers">Преподаватели</router-link>).
      </li>
      <li>
        <strong>Расписание на заданный день недели для указанной группы?</strong><br />
        Выберите группу и день недели, чтобы увидеть соответствующие занятия (см. 
        <router-link to="/schedule">Расписание</router-link>).
      </li>
      <li>
        <strong>Сколько студентов обучается на каждом курсе в указанном классе?</strong><br />
        Перейдите к разделу групп и отфильтруйте по нужному курсу или классу (см. 
        <router-link to="/groups">Группы</router-link>).
      </li>
    </ul>

    <h2>Сводные ведомости успеваемости</h2>
    <p>
      Необходимо предусмотреть возможность получения документа, представляющего собой сводные ведомости успеваемости
      за семестр по каждой группе, включая сведения о среднем балле группы за семестр.
      <br />
      Например, вы можете найти это в разделе
      <router-link to="/grade-report">Сводные ведомости</router-link>.
    </p>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  created() {
    console.log('HomeView has been created')
  }
}
</script>

<style scoped>
h1 {
  color: #333;
  margin-bottom: 10px;
}
h2 {
  margin-top: 20px;
  color: #444;
}
ul {
  list-style: disc;
  padding-left: 20px;
  margin-bottom: 20px;
}
li {
  margin-bottom: 10px;
}
</style>
