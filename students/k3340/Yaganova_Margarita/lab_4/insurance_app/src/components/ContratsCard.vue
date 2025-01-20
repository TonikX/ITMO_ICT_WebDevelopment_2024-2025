<template>
<div class="card">
    <div class="card-header">
        <router-link :to="{ name: 'contract-details', params: { contractNumber: dict['id'] }}">{{ dict['id'] }}</router-link>
    </div>
    <div class="card-body">
    <ul>
        <template v-for="(value, key) in dict" :key="key">
            <li v-if="key!=='id'">{{ key }} : {{ value }}</li>
        </template>
    </ul>
    </div>
</div>
</template>

<script>
import { routeLocationKey } from 'vue-router';

export default {
    props: {
        dict: {
            type: Object,
            required: true,
        },
    },
    components: { routeLocationKey }
};
</script>

