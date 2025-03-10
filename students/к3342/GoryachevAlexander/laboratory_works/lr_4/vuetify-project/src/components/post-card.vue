<template>
  <v-card
    class="mx-auto"
  >
    <v-img
      height="200px"
      :src="url"
      class='mb-3'
      cover
    ></v-img>

    <v-card-subtitle class="text-overline mb-1">
        {{ post.category }}
    </v-card-subtitle>

    <v-card-title>
      {{ post.title }}
    </v-card-title>

    <v-card-subtitle>
      Автор: {{ post.author.username}}
    </v-card-subtitle>

    <v-card-actions>
      <v-btn
        color="indigo-lighten-3"
        text="Подробнее"
        :to="`/blogs/${post.id}`"
      ></v-btn>

      <v-spacer></v-spacer>

      <v-btn
        :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
        @click="show = !show"
      ></v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <v-divider></v-divider>

        <v-card-text>
          {{ croppedContent }}
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>
<script setup>

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})

const show = ref(false)

const croppedContent = computed(() => {
  return props.post.content.slice(0, 200).concat('...')
})

const url = computed(() => props.post?.image_url ? props.post.image_url : 'https://apptor.studio/assets/cache/images/600-856x600-629.png');

</script>
