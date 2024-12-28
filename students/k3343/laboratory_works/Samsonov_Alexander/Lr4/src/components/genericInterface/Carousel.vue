<template>
  <h1>{{ carouselData.carouselData.header }}</h1>
  <div :id=carouselSelector class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner">
      <div
          class="carousel-item"
          :class="{ active: index === 0 }"
          v-for="(group, index) in groupedData"
          :key="index"
      >
        <div class="row">
          <div class="col-md-3" v-for="item in group" :key="item.id">
            <ListCard
                :recipe="item"
            />
          </div>
        </div>
      </div>
    </div>

    <button
        class="carousel-control-prev"
        type="button"
        :data-bs-target="'#'+carouselSelector"
        data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
        class="carousel-control-next"
        type="button"
        :data-bs-target="'#'+carouselSelector"
        data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
  <hr>
</template>

<script setup>
import ListCard from "@/components/genericInterface/ListCard.vue";
import {onMounted, ref} from "vue";

const groupedData = ref(null)
const carouselData = defineProps(["carouselData"]);
const carouselSelector = ref(null)

const batchSplit = (batch, split) => {
  const array = []

  const limiter = batch.length;
  for (let i = 0; i < limiter; i += split) {
    array.push(batch.slice(i, i + split));
  }
  return array;
}

onMounted(() => {
      groupedData.value = batchSplit(carouselData.carouselData.recipes, 4)
      carouselSelector.value = `carousel--${carouselData.carouselData.id}`
    }
)
</script>