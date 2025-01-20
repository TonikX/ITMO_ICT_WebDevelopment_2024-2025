<template>
  <div>
    <object-list :title="pageTitle" :info-array="infoArray" title-key="short_name"></object-list>
  </div>

  <div class="form-container">
     <form @submit.prevent="submit">
        <label for="fullName">Full name:</label>
        <input type="text" id="fullName" v-model="enterpriseData.full_name" required class="form-control">

        <label for="shortName">Short name:</label>
        <input type="text" id="shortName" v-model="enterpriseData.short_name" required class="form-control">

        <label for="code">Code:</label>
        <input type="number" id="code" v-model="enterpriseData.code" required class="form-control">

        <label for="bankDetail">Bank details:</label>
        <input type="number" id="bankDetail" v-model="enterpriseData.bank_details" required class="form-control">

        <label for="address">Address:</label>
        <input type="text" id="address" v-model="enterpriseData.address" class="form-control">

        <label for="specialization">Specialization:</label>
            <select class="form-select" v-model="enterpriseData.specialization" id="specialization" required multiple>
                <option v-for="spec in specializations" :key="spec.id" :value="spec.id">{{ spec.title }}</option>
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
      pageTitle: 'Enterprises',
      infoArray: [],
      specializations: [],
      enterpriseData: {
        full_name: '',
        short_name: '',
        code: null,
        bank_details: null,
        address: '',
        specialization: null
      }
    };
  },
  methods: {
    submit() {
        console.log(this.enterpriseData);
        axios.post('http://127.0.0.1:8000/enterprises/', this.enterpriseData)
            .then(response => {window.location.reload()})
    }
  },
  async mounted() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/enterprises/')
        this.infoArray = response.data;
        const spec_response = await axios.get('http://127.0.0.1:8000/specializations/')
        this.specializations = spec_response.data;
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