<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {fetchWithLoading} from "@/composables/serverActions.js"
import StepsList from "@/components/workoutPage/stepsList.vue";
import TagsList from "@/components/workoutPage/tagsList.vue";
import {isAuthenticated} from "@/composables/tokenActions.js";
import axiosInstance from "@/services/axios.js";
import CommentCard from "@/components/workoutPage/commentCard.vue";
import CommentForm from "@/components/workoutPage/commentForm.vue";


// workoutState
const workoutPath = useRoute().params.workoutId;
const workoutData = ref(null)
const wLoading = ref(true);
const wError = ref(null);

// flags
const isLiked = ref(false);
const isDone = ref(false);
const canEdit = ref(false);

// comments state
const CommentsData = ref(null)
const cLoading = ref(true);
const cError = ref(null);


function ytId(str) {
  const match = str.match(/=(.*?)&/);
  return match ? match[1] : null;
}

function ytThumbnail(str) {
  const match = str.match(/=(.*?)&/);
  if (match) {
    return `https://img.youtube.com/vi/${match[1]}/maxresdefault.jpg`;
  }
  return 'https://placehold.co/600x400';
}

async function getFlags() {
  isLiked.value = (await axiosInstance.get(`workouts/${workoutData.value.id}/favorite/`)).data
  isDone.value = (await axiosInstance.get(`workouts/${workoutData.value.id}/done/`)).data
  canEdit.value = (await axiosInstance.get(`workouts/${workoutData.value.id}/canEdit/`)).data
}

function like() {
  axiosInstance.post(`/workouts/${workoutData.value.id}/favorite/`)
  isLiked.value = !isLiked.value
}

function done() {
  axiosInstance.post(`/workouts/${workoutData.value.id}/done/`)
  isDone.value = !isDone.value
}


const onCommentSubmitted = async (result) => {
  await fetchWithLoading(`comment/workout_comment/${workoutData.value.id}`, CommentsData, cLoading, cError)
  CommentsData.value.push(await result)
}

onMounted(async () => {
  await fetchWithLoading(`workouts/${workoutPath}`, workoutData, wLoading, wError);
  await fetchWithLoading(`comment/workout_comment/${workoutData.value.id}`, CommentsData, cLoading, cError)
  await getFlags()
})
</script>

<template>
  <div class="container">
    <div v-if="wLoading">Loading workout...</div>
    <div v-else-if="wError">{{ wError }}</div>
    <div v-else>
      <div class="row">
        <div class="col-8">
          <h1>{{ workoutData.title }}</h1>

          <p>{{ workoutData.description }}</p>
        </div>
        <div class="col-4">
          <p>Rating: {{ workoutData.rating !== null ? `${workoutData.rating.toFixed(1)}/10` : 'no data' }}</p>
          <p>Author: {{ workoutData.author.username }}</p>
          <div v-if="isAuthenticated">
            <button
                class="btn"
                :class="isLiked ? 'btn-success' : 'btn-outline-success'"
                @click="like()">
              {{ isLiked ? 'Liked' : 'Like' }}
            </button>
            <button
                class="btn ms-3"
                :class="isDone ? 'btn-primary' : 'btn-outline-primary'"
                @click="done()">
              {{ isDone ? 'Completed' : 'Mark as Done' }}
            </button>
            <div class="my-3" v-if="canEdit">
              <!-- Create Resource Button -->
              <router-link
                  :to="`/workouts/${workoutData.id}/edit`"
                  class="btn btn-success my-1 mx-1"
              >
                <i class="bi bi-plus-circle"></i> Edit the post
              </router-link>

              <!-- Delete Resource Button -->
              <router-link
                  :to="`/workouts/${workoutData.id}/delete`"
                  class="btn btn-danger my-1 mx-1"
              >
                <i class="bi bi-trash"></i> Delete the post
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <img :src="ytThumbnail(workoutData.video_link)" alt="workoutData.title" class="img-fluid rounded">

      <hr>
      <tags-list :tags="workoutData.tags_display"/>


      <steps-list :workout-list="workoutData.steps_display"/>

      <div class="container my-5" v-if="ytId(workoutData.video_link)">
        <div class="text-center">
          <h1 class="mb-4">Watch the video version here</h1>
          <div class="embed-responsive embed-responsive-16by9">
            <iframe
                width="800" height="460"
                :src="`https://www.youtube.com/embed/${ytId(workoutData.video_link)}`"
                class="embed-responsive-item"
                frameborder="0"
                allowfullscreen>
            </iframe>
          </div>
        </div>
      </div>
    </div>

    <div v-if="cLoading">Loading comments...</div>
    <div v-else-if="wError">{{ cError }}</div>
    <div v-else>
      <CommentForm :workout_id="workoutData.id" @submitComment="onCommentSubmitted" v-if="isAuthenticated"/>
      <comment-card v-for="Comment in CommentsData" :key="Comment.id" :comment="Comment"/>

    </div>
  </div>
</template>

<style scoped>

</style>