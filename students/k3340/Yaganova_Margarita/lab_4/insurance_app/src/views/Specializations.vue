<template>
  <div>
    <object-list :title="pageTitle" :info-array="infoArray" title-key="title"></object-list>
  </div>

  <div class="form-container">
     <form @submit.prevent="submit">
      <label for="textInput">Enter specialization:</label>
      <input type="text" id="textInput" v-model="inputText" required class="form-control">
      <button class="btn btn-primary" type="submit">Enter</button>
    </form>
  </div>
</template>

<script>
import ObjectList from '@/components/ObjectList.vue';
import axios from 'axios';


export default {
  components: {
    ObjectList,
  },
  data() {
    return {
      pageTitle: 'Specializations',
      infoArray: [],
      inputText: '',
    };
  },
  methods: {
    submit() {
        axios.post('http://127.0.0.1:8000/specializations/', { title: this.inputText })
            .then(response => {window.location.reload()})
    }
  },
  async mounted() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/specializations/')
        this.infoArray = response.data;
    } catch (error) {
        console.error(error)
    }
  }
};
</script>

<style>
.form-container {
    margin: 20px;
}

.form-control {
    margin: 7px 0px 7px 0px;
}
</style>