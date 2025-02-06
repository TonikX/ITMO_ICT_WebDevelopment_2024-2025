<script>
import WarriorForm from "@/components/WarriorForm.vue";
import WarriorList from "@/components/WarriorList.vue";
import axios from "axios";

export default {
    components: {
        WarriorForm, WarriorList,
    },
    data() {
        return {
            warriors: [],

        }
    },
    methods: {
        async fetchWarriors() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/warriors/")
                console.log(response.data)
                this.warriors = response.data
            } catch (e) {
                console.log(e)    
            }
        }
    },
    mounted() {
        this.fetchWarriors()
    },
}
</script>


<template>
    <div class="app">
        <h1>Войны</h1>
        <button @click="fetchWarriors">Получить список войнов</button>
        <WarriorForm/>
        <WarriorList :warriors="warriors"/>
    </div>
</template>