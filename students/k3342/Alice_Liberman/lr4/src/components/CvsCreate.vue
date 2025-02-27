<template>
  <div class="container mt-5">
    <h2 class="mb-4">Submit Your Text</h2>
    <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="inputText" class="form-label">Enter Text</label>
        <input
          type="text"
          class="form-control"
          id="inputText"
          v-model="textInput"
          required
          placeholder="Enter some text"
        />
        <div class="invalid-feedback">
          Please provide some text.
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
import axiosInstance from "@/services/axios.js";
import router from "@/router/index.js";

export default {
  name: 'CvsCreate',
  data() {
    return {
      textInput: '',
    };
  },
  methods: {
    async handleSubmit() {
      if (!this.textInput) {
        alert('Please enter some text before submitting.');
        return;
      }

      try {
        const response = await axiosInstance.post('/cvs/', { content_blob: this.textInput });
        console.log('Success:', response.data);
        alert('Text submitted successfully!');
        this.$emit('success');
        this.textInput = '';
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to submit text. Please try again.');
      }
    },
  },
};
</script>

<style scoped>
</style>