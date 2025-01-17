<template>
  <div>
    <Header />
    <h1>Добро пожаловать в систему управления газетами!</h1>
  </div>
</template>

<script>
import Header from "../components/Header.vue";

export default {
  components: {
    Header,
  },
};
</script>

<style scoped>
h1 {
  font-size: 2em;
}

p {
  font-size: 1.2em;
}

div {
  margin-top: 20px;
}

router-link {
  margin-right: 20px;
  font-size: 1.1em;
  text-decoration: none;
}
</style>
