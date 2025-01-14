<template>
   <div class="app">
     <h1>Портал информации о войнах в онлайн РПГ</h1>
     <button v-on:click="fetchWarriors">Получить список войнов</button> <!-- Кнопка вызывает функцию получения списка данных (функция fetchWarriors объявлена в блоке "methods") -->
     <warrior-form/> <!-- Встраивание компонента формы -->
     <warrior-list
         v-bind:warriors="warriors"
     /> <!-- Встраивание компонента вызывающего список объектов. v-bind - директива служит для так называемой data binding -- привязки данных (данные объявляются в блоке данных data() (см. код ниже)). -->
   </div>
</template>

<script>
import WarriorForm from "@/components/WarriorForm.vue";
import WarriorList from "@/components/WarriorList.vue";
import axios from "axios";

export default {
 components: {
   WarriorForm, WarriorList
 },

 data() { // data - это функция, которая возвращает объект с данными
   return {
     warriors: [], // Массив данных (передается в компонент WarriorList, получает данные средствами функции fetchWarriors
   }
 },
 methods: { // methods. Это объект, который содержит список Javascript функций, которые должны выполняться в зависимости от того, какие действия производит пользователь.
   async fetchWarriors () { // асинхронная функция для получения данных
     try {
       const response = await axios.get('http://62.109.28.95:8890/warriors/list/') // Выполнение GET-запроса Backend-серверу. Запрос вернет JSON.
       console.log(response.data.results)
       this.warriors = response.data.results // Массив данных warriors из блока(функции) data() получает значением результат только-что выполненного запроса
     } catch (e) {
       alert('Ошибка')
     }
   }

 },
 mounted() {
   this.fetchWarriors() // Vue вызывает хук mount(), когда компонент добавляется в DOM.  В данном примере это позволяет вызвать fetchWarriors для получения списка воинов до отрисовки страницы в браузере, благодаря этому страница загружается с уже полученными ранее данными.

 }
}
</script>
