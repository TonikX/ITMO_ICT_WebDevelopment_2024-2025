<template>
  <div class="app">
    <h1>Портал информации о войнах в онлайн РПГ</h1>
    <button v-on:click="fetchWarriors">Получить список войнов</button>
    <warrior-form /> <!-- 引入 WarriorForm 组件 -->
    <warrior-list v-bind:warriors="warriors" /> <!-- 引入 WarriorList 组件 -->
  </div>
</template>

<script>
import WarriorForm from "@/components/WarriorForm.vue";
import WarriorList from "@/components/WarriorList.vue";
import axios from "axios";

export default {
  components: {
    WarriorForm,
    WarriorList,
  },
  data() {
    return {
      warriors: [], // 存储从后端获取的战士数据
    };
  },
  methods: {
    async fetchWarriors() {
      try {
        const response = await axios.get('http://62.109.28.95:8890/warriors/list/'); // 获取战士数据
        console.log(response.data.results);
        this.warriors = response.data.results; // 将数据赋值给 warriors 数组
      } catch (e) {
        alert('Ошибка');
      }
    },
  },
  mounted() {
    this.fetchWarriors(); // 在组件挂载后获取数据
  },
};
</script>

<style scoped>
/* 可根据需要添加样式 */
</style>
