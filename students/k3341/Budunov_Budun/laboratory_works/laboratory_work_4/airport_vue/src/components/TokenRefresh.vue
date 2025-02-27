<script>
import axios from 'axios'

export default {
  name: 'TokenRefresher',
  data () {
    return {
      refreshInterval: null
    }
  },
  methods: {
    async refreshToken () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.post('/api/token/refresh/', {
          refresh: tokens.refresh
        })
        const newTokens = {
          access: response.data.access,
          refresh: tokens.refresh
        }
        localStorage.setItem('tokens', JSON.stringify(newTokens))
      } catch (error) {
        this.$router.push('/login')
      }
    },
    startRefreshInterval () {
      this.refreshInterval = setInterval(this.refreshToken, 55 * 60 * 1000)
    },
    stopRefreshInterval () {
      clearInterval(this.refreshInterval)
    }
  },
  mounted () {
    this.startRefreshInterval()
  },
  beforeUnmount () {
    this.stopRefreshInterval()
  }
}
</script>

<template>
  <div></div>
</template>
