<template>
  <v-container>
    <HeaderButtons />

    <v-row justify="center">
      <v-col cols="12" md="8">
        <h1 class="text-center mb-4">Airport Management System</h1>
        <v-img
            class="mx-auto"
            src="https://th.bing.com/th/id/R.e2a55a7030c61d4b6586e586732c484a?rik=w10n%2f9B7sV5%2fzw&riu=http%3a%2f%2fwww.flyertalk.com%2fattachments%2fimg_20161016_103647-jpg.636521%2f&ehk=u%2bYpO5wY0l%2f0x1%2fq0x2g6o381pK3K3n%2f5xR1Q%3d&risl=&pid=ImgRaw&r=0"
            max-width="80%"
            contain
        ></v-img>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import HeaderButtons from '@/components/HeaderButtons.vue'

export default {
  name: 'HomeView',
  components: {
    HeaderButtons
  }
}
</script>

<style scoped>
</style>
