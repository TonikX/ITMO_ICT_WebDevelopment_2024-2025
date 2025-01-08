<template>
  <v-app-bar color="primary">
    <v-container class="d-flex align-center">
      <v-app-bar-title>
        Автобусный парк
      </v-app-bar-title>

      <v-tabs v-model="currentTab">
        <v-tab
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          :value="item.path"
        >
          {{ item.title }}
        </v-tab>
      </v-tabs>

      <v-spacer></v-spacer>

      <v-btn
        variant="text"
        to="/profile"
        class="ml-2"
      >
        Профиль
      </v-btn>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  name: 'AppHeader',

  data: () => ({
    currentTab: null,
    menuItems: [
      { title: 'Водители', path: '/drivers' },
      { title: 'Автобусы', path: '/buses' },
      { title: 'Маршруты', path: '/routes' },
      { title: 'Назначения', path: '/assignments' }
    ]
  })
}
</script> 