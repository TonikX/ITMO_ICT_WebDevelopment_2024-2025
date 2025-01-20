<template>
  <div>
    <object-list :title="pageTitle" :info-array="infoArray" title-key="name"></object-list>
  </div>

  <div class="form-container">
     <form @submit.prevent="submit">
        <label for="fullName">Full name:</label>
        <input type="text" id="fullName" v-model="clientData.name" required class="form-control">

        <label for="age">Age:</label>
        <input type="number" id="age" v-model="clientData.age" required class="form-control">

        <label for="risk_category">Risk category:</label>
            <select class="form-select" v-model="clientData.risk_category" id="risk_category" required>
                <option v-for="cat in categories">{{ cat }}</option>
            </select>
        <br>

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
      pageTitle: 'Clients',
      infoArray: [],
      categories: ["first", "second", "highest"],
      clientData: {
        name: '',
        age: null,
        risk_category: null
      }
    };
  },
  methods: {
    submit() {
        console.log(this.enterpriseData);
        axios.post('http://127.0.0.1:8000/clients/', this.clientData)
            .then(response => {window.location.reload()})
    }
  },
  async mounted() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/clients/')
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