<template>
  <svg xmlns="http://www.w3.org/2000/svg" class="sprite-container" aria-hidden="true" display="none">
    <symbol id="icon-logout" viewBox="0 0 24 24">
      <path d="M8.5 10c-.276 0-.5-.448-.5-1s.224-1 .5-1 .5.448.5 1-.224 1-.5 1"/>
      <path d="M10.828.122A.5.5 0 0 1 11 .5V1h.5A1.5 1.5 0 0 1 13 2.5V15h1.5a.5.5 0 0 1 0 1h-13a.5.5 0 0 1 0-1H3V1.5a.5.5 0 0 1 .43-.495l7-1a.5.5 0 0 1 .398.117M11.5 2H11v13h1V2.5a.5.5 0 0 0-.5-.5M4 1.934V15h6V1.077z"/>
    </symbol>

    <symbol id="icon-blog" viewBox="0 0 24 24">
      <path
        d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783"/>
    </symbol>

    <symbol id="icon-profile" viewBox="0 0 24 24">
      <path
        d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4m-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10s-3.516.68-4.168 1.332c-.678.678-.83 1.418-.832 1.664z"/>
    </symbol>
    <symbol id="icon-dashboard" viewBox="0 0 24 24">
      <path
        d="M8 4a.5.5 0 0 1 .5.5V6a.5.5 0 0 1-1 0V4.5A.5.5 0 0 1 8 4M3.732 5.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707M2 10a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 10m9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5m.754-4.246a.39.39 0 0 0-.527-.02L7.547 9.31a.91.91 0 1 0 1.302 1.258l3.434-4.297a.39.39 0 0 0-.029-.518z"/>
      <path fill-rule="evenodd"
            d="M0 10a8 8 0 1 1 15.547 2.661c-.442 1.253-1.845 1.602-2.932 1.25C11.309 13.488 9.475 13 8 13c-1.474 0-3.31.488-4.615.911-1.087.352-2.49.003-2.932-1.25A8 8 0 0 1 0 10m8-7a7 7 0 0 0-6.603 9.329c.203.575.923.876 1.68.63C4.397 12.533 6.358 12 8 12s3.604.532 4.923.96c.757.245 1.477-.056 1.68-.631A7 7 0 0 0 8 3"/>
    </symbol>
    <symbol id="icon-workout" viewBox="0 0 24 24">
      <path
        d="M4 4.5a.5.5 0 0 1 .5-.5H6a.5.5 0 0 1 0 1v.5h4.14l.386-1.158A.5.5 0 0 1 11 4h1a.5.5 0 0 1 0 1h-.64l-.311.935.807 1.29a3 3 0 1 1-.848.53l-.508-.812-2.076 3.322A.5.5 0 0 1 8 10.5H5.959a3 3 0 1 1-1.815-3.274L5 5.856V5h-.5a.5.5 0 0 1-.5-.5m1.5 2.443-.508.814c.5.444.85 1.054.967 1.743h1.139zM8 9.057 9.598 6.5H6.402zM4.937 9.5a2 2 0 0 0-.487-.877l-.548.877zM3.603 8.092A2 2 0 1 0 4.937 10.5H3a.5.5 0 0 1-.424-.765zm7.947.53a2 2 0 1 0 .848-.53l1.026 1.643a.5.5 0 1 1-.848.53z"/>
    </symbol>
  </svg>
  <v-navigation-drawer :width="320"
                       location="top"
                       permanent>
    <v-list
      class="d-flex flex-row"
      density="compact"
      nav
    >
      <v-list-item
        lines="two"
        subtitle="Logged in"
        :prepend-avatar="`${user.imageUrl}`"
        :title="`${user.username}`"
      ></v-list-item>
      <v-divider></v-divider>
      <v-list-item to="/workouts/all" class="d-flex align-center">
        <!-- Text content -->
        <span>Тренировки</span>
        <!-- SVG icon placed to the right -->
        <svg class="icon" aria-hidden="true" focusable="false">
          <use href="#icon-workout"/>
        </svg>
      </v-list-item>
      <v-list-item to="/dashboard" class="d-flex align-center">
        <!-- Text content -->
        <span>Личный кабинет</span>
        <!-- SVG icon placed to the right -->
        <svg class="icon" aria-hidden="true" focusable="false">
          <use href="#icon-profile"/>
        </svg>
      </v-list-item>
      <v-list-item to="/blogs/all" class="d-flex align-center">
        <!-- Text content -->
        <span>Статьи</span>
        <!-- SVG icon placed to the right -->
        <svg class="icon" aria-hidden="true" focusable="false">
          <use href="#icon-blog"/>
        </svg>
      </v-list-item>

      <v-list-item to="/logout" class="d-flex align-center">
        <!-- Text content -->
        <span>Выйти</span>
        <!-- SVG icon placed to the right -->
        <svg class="icon" aria-hidden="true" focusable="false">
          <use href="#icon-logout"/>
        </svg>
      </v-list-item>

      <v-list-item>
        <ThemeSwitcher/>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>


<script setup>
import {useAppStore} from '@/stores/app';
import {ref} from 'vue';
import ThemeSwitcher from './theme-switcher.vue';

const store = useAppStore();

const user = computed(() => JSON.parse(store.user))
</script>
