<template>
<div class="card">
    <div class="card-header">{{ dict[title] }}</div>
    <div class="card-body" v-if="Object.keys(dict).length > 2">
    <ul>
        <template v-for="(value, key) in dict" :key="key">
            <li v-if="key!==title && key!=='id'">{{ value }}</li>
        </template>
    </ul>
    </div>
</div>
</template>

<script>
export default {
  props: {
    dict: {
      type: Object,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
};
</script>

