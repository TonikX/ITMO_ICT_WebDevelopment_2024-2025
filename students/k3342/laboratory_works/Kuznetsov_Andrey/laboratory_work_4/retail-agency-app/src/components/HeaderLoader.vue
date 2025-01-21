<template>
  <header>
    <div class="theme-switch-container" aria-label="Theme switch">
      <label class="theme-switch">
        <input type="checkbox" id="themeSwitcher" @change="toggleTheme" />
        <span class="slider"></span>
      </label>
    </div>

    <nav>
      <ul class="menu">
        <li><router-link to="/profile" aria-label="Go to your account page">Account</router-link></li>
        <li><router-link to="/messages" aria-label="View your messages">Messages</router-link></li>
        <li><router-link to="/search" aria-label="Search the website">Search</router-link></li>
        <li><router-link to="/about" aria-label="Learn more about us">About</router-link></li>
        <li><router-link to="/contact" aria-label="Contact us">Contact</router-link></li>
      </ul>
    </nav>

    <a class="logo" href="/" aria-label="Go to homepage">
      <svg class="logo-icon">
        <use xlink:href="#homeIcon"></use>
      </svg>
    </a>
  </header>
</template>

<script>
export default {
  name: 'HeaderLoader',
  data() {
    return {
      themeChecked: false,
    };
  },
  mounted() {
    this.initTheme();
    this.setActiveMenu();
  },
  methods: {
    initTheme() {
      const savedTheme = localStorage.getItem('theme') || ''; 
      if (savedTheme === 'vanilla-dark') {
        this.themeChecked = true;
        document.documentElement.setAttribute('data-theme', 'vanilla-dark'); 
      } else {
        document.documentElement.removeAttribute('data-theme'); 
      }
    },

    toggleTheme() {
      if (this.themeChecked) {
        document.documentElement.setAttribute('data-theme', 'vanilla-dark'); 
        localStorage.setItem('theme', 'vanilla-dark'); 
        this.themeChecked = false;
      } else {
        document.documentElement.removeAttribute('data-theme'); 
        localStorage.removeItem('theme');
        this.themeChecked = true;
      }
    },

    setActiveMenu() {
      const currentPath = window.location.pathname;
      const menuItems = document.querySelectorAll('.menu li a');
      const authPath = '/auth';
      const profilePath = '/profile';

      menuItems.forEach((item) => {
        const linkPath = item.getAttribute('href').replace('..', '');

        if (linkPath === currentPath) {
          item.parentElement.classList.add('active');
        } else {
          item.parentElement.classList.remove('active');
        }

        if (currentPath === authPath && linkPath === profilePath) {
          item.parentElement.classList.add('active');
        }
      });
    }
  },
};
</script>


<style scoped>
@import url('../assets/css/themes.css');

header{
    background-color: var(--secondary-color);
    position: fixed;
    width: 100%;
    height: 70px;
    background-size: cover;
    background-position: center;
    z-index: 1000;
}

.top-bar {
    background-color: var(--secondary-color);
    height: 100%;
}

.menu {  
    float: right;
    list-style-type: none;
    margin-top: 25px;
}

.menu li{
    display: inline-block;
}

.menu li a{
    text-decoration: none;
    color: var(--primary-color);
    padding: 5px 20px;
    transition: 0.6s ease;
}

.menu li a:hover{
    background-color: var(--primary-color);
    color: var(--primary-back);
}

.menu li.active a{
    background-color: var(--primary-color);
    color: var(--secondary-color);
}

.logo {
    position: absolute;
    margin-top: 12px;
    float: left;
}

.logo-icon {
    width: 50px;
    height: 50px;
    stroke: var(--primary-color);
}

.theme-switch-container {
    display: inline-block;
    margin-left: 60px;
    position: absolute; 
    height: 100%; 
}

.theme-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 25px;
    
    top: 50%;
    transform: translateY(-50%);
}

.theme-switch input {
    opacity: 0; 
    position: absolute; 
    z-index: 2; 
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    cursor: pointer;
}

.theme-switch .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--hover-color);
    transition: 0.4s;
    border-radius: 25px;
    z-index: 1;
}

.theme-switch .slider:before {
    position: absolute;
    content: "";
    height: 17px;
    width: 17px;
    left: 4px;
    bottom: 4px;
    background-color: var(--text-color);
    transition: 0.4s;
    border-radius: 50%;
}

.theme-switch input:checked + .slider:before {
    transform: translateX(24px);
}
</style>
