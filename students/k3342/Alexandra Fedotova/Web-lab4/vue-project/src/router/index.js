import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import Login from '../views/Login.vue';
import Register from '../views/Registration.vue';
import WorkoutSearch from '../views/WorkoutSearch.vue';
import WorkoutDetails from '../views/WorkoutDetails.vue';
import Blog from '../views/Blog.vue';
import Post from '../components/Blog/Post.vue';
import Personal_Acc from "@/views/Personal_Acc.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/acc',
      name: 'Account',
      component: Personal_Acc,
      props: true,
    },
    {
      path: '/search',
      name: 'Search',
      component: WorkoutSearch,
      props: true,
    },
    {
      path: '/workout',
      name: 'Workout',
      component: WorkoutDetails,
    },
    {
      path: '/blog',
      name: 'Blog',
      component: Blog,
    },
    {
      path: '/post',
      name: 'Post',
      component: Post,
      props: true
    },

  ],
});

export default router;
