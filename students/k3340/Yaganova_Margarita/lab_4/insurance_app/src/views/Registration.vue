<template>
    <div class="container col-md-8">
        <h1>Registration</h1>
        <user-form :mode="'register'"></user-form>
    </div>
</template>

<script>
import UserForm from '@/components/UserForm.vue';

export default {
    components: {
        UserForm
    }
}
</script>

<style>
.container {
    margin: 10px;
}
</style>