<template>
    <div class="reader-box">
        <div class="reader-ticket">
            {{ reader.reading_ticket_number }}
        </div>
        <div class="reader-full-name">
        <router-link
        :to="{path: `/reader/${reader.id}`}"
        v-bind:reader.id="id" >
            {{ reader.full_name }}
        </router-link>
        </div>
        <div class="reader-phone">
            Номер телефона: {{ reader.phone_number }}
        </div>
        <button class="delete-button" @click="$emit('remove', reader)" style="color: red;">Удалить</button>
    </div>
</template>

<script>
export default {
    props: {
        reader: {
            type: Object,
            required: true,
        }
    },
}
</script>

<style scoped>
.reader-box {
    padding: 15px;
    margin-top: 20px;
    border: 2px solid whitesmoke;
}

</style>