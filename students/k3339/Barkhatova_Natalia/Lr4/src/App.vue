<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <a href="#" @click.prevent="handleLogout">Logout</a>
    </nav>
    <router-view/>
  </div>
</template>



<
<script>
import {useAuthStore} from '@/stores/auth';
import {useRouter} from 'vue-router';

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const handleLogout = async () => {
      await authStore.logout();
      router.push('/login');
    };
    return {
      handleLogout
    };
  }
};
</script>


<style>
body {
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #333;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

nav {
  background-color: #800020;
  padding: 10px 20px;
  text-align: center;
}

nav a {
  color: #FFF8DC;
  text-decoration: none;
  margin: 0 15px;
  font-size: 18px;
  transition: color 0.3s;
}

nav a:hover {
  color: #FFAA33;
}

router-link {
  cursor: pointer;
}

button {
  font-family: 'Great Vibes', cursive;
  background-color: #FFAA33;
  border: none;
  padding: 10px 20px;
  color: #fff;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  margin-top: 10px;
}

button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -75%;
  width: 50%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.5);
  transform: skewX(-25deg);
  transition: 0.6s;
}

button:hover::before {
  left: 125%;
}
html, body, #app{
  height: 100%;
  width: 100%;
}
</style>
