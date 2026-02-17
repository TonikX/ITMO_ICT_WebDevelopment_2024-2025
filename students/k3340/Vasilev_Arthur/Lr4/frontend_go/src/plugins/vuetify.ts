import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#7C3AED',
          secondary: '#EC4899',
          accent: '#06B6D4',
          error: '#EF4444',
          info: '#3B82F6',
          success: '#10B981',
          warning: '#F59E0B',
          surface: '#F5F3FF',
          background: '#FAFAFA',
        },
      },
    },
  },
})

