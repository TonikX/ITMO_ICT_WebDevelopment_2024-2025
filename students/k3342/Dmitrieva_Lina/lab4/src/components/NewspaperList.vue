<template>
  <div>
    <Filters @filter="applyFilter" />
    <div class="newspaper-list">
      <NewspaperCard v-for="newspaper in filteredNewspapers" :key="newspaper.id" :newspaper="newspaper" />
    </div>
  </div>
</template>

<script>
import NewspaperCard from "../components/NewspaperCard.vue";
import Filters from "../components/Filters.vue";
import { getNewspapers } from "../api/api";

export default {
  components: {
    NewspaperCard,
    Filters,
  },
  data() {
    return {
      newspapers: [],
      filteredNewspapers: [],
    };
  },
  async created() {
    try {
      const response = await getNewspapers();
      this.newspapers = response.data;
      this.filteredNewspapers = this.newspapers;
    } catch (error) {
      console.error("Ошибка при загрузке газет:", error);
    }
  },
  methods: {
    applyFilter(filters) {
      this.filteredNewspapers = this.newspapers.filter((newspaper) => {
        let match = true;

        if (filters.search && !newspaper.name.toLowerCase().includes(filters.search.toLowerCase())) {
          match = false;
        }

        if (filters.price && newspaper.price < filters.price) {
          match = false;
        }

        if (filters.quantity && newspaper.quantity < filters.quantity) {
          match = false;
        }

        return match;
      });
    },
  },
};
</script>

<style scoped>
.newspaper-list {
  display: flex;
  flex-wrap: wrap;
}
</style>
