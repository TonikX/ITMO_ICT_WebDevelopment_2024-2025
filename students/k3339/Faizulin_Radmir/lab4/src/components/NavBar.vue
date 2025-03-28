<template>
  <nav>
    <ul class="horizontal-menu">
      <li v-for="(menu, index) in menus" :key="index" class="dropdown">
        <span>{{ menu.label }}</span>
        <ul class="dropdown-menu">
          <li v-for="(item, i) in menu.items" :key="i">
            <router-link :to="item.route">{{ item.label }}</router-link>
          </li>
        </ul>
      </li>
      <p v-if="hasToken">
        <router-link to="/logout" class="logout-link">Log out</router-link>
      </p>
      <p v-else>
        <router-link to="/login" class="logout-link">Log in</router-link>
      </p>
    </ul>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      menus: [
        {
          label: 'Books',
          items: [
            { label: 'All Books', route: '/books' },
            { label: 'Add new book', route: '/books/new' },
          ]
        },
        {
          label: 'Readers',
          items: [
            { label: 'All Readers', route: '/readers' },
            { label: 'Add new reader', route: '/readers/new' }
          ]
        },
        {
          label: 'Assignments',
          items: [
            { label: 'All Assignments', route: '/assignments'},
            { label: 'Add new Assignments', route: '/assignments/new'},
          ]
        },
        {
          label: 'Halls',
          items: [
                { label: 'All Halls', route: '/halls'},
                { label: 'Add new Halls', route: '/halls/new'}
          ]
        },
        {
          label: 'Copies',
          items: [
                { label: 'All Copies', route: '/copies'},
                { label: 'Add new Copies', route: '/copies/new'},
          ]
        }
      ]
    }
  },
  computed: {
    hasToken() {
      return !!localStorage.getItem('token');
    }
  }
}
</script>

<style scoped>
.horizontal-menu {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  font-family: Arial, sans-serif;
}

.horizontal-menu li {
  position: relative;
}

.horizontal-menu li .dropdown-menu {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  z-index: 1;
}

.horizontal-menu li:hover .dropdown-menu {
  display: block;
}

.horizontal-menu li:hover {
  background-color: #ddd;
}

.horizontal-menu li:hover > span {
  background-color: #ddd;
}

.horizontal-menu li span {
  display: block;
  color: black;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

.horizontal-menu li .dropdown-menu a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.horizontal-menu li .dropdown-menu a:hover {
  background-color: #f1f1f1;
}



nav {
  background-color: #f0f0f0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
}


.logout-link {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: black;
  text-decoration: none;
}

.logo {
  height: 50px; /* Настройте высоту вашего логотипа */
  width: auto; /* Автоматическое определение ширины */
}
</style>
