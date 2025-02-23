import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import 'vuetify/dist/vuetify.min.css';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#0d47a1', // Dark blue
        secondary: '#424242', // Dark gray
        accent: '#2962ff', // Brighter blue
        error: '#FF5252',
        info: '#29b6f6', // light blue
        success: '#388e3c', // green
        warning: '#ffc400', // yellow
        background: "#f2f2f2", // light gray
      },
    },
  },
});

