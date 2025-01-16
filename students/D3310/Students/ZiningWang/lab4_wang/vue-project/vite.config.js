// import { fileURLToPath, URL } from 'node:url'

// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// import vueDevTools from 'vite-plugin-vue-devtools'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [
//     vue(),
//     vueDevTools(),
//   ],
//   resolve: {
//     alias: {
//       '@': fileURLToPath(new URL('./src', import.meta.url))
//     },
//   },
// })

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // 配置代理，确保前端请求可以被转发到后端服务器
      '/warriors': {
        target: 'http://62.109.28.95:8890', // 后端服务器地址
        changeOrigin: true,  // 改变源头，解决跨域问题
        secure: false,  // 如果是https的请求，设置为true
        rewrite: (path) => path.replace(/^\/warriors/, '/warriors')  // 可选：路径重写
      },
      '/warrior': {
        target: 'http://62.109.28.95:8890', // 后端服务器地址
        changeOrigin: true,  // 改变源头，解决跨域问题
        secure: false,  // 如果是https的请求，设置为true
        rewrite: (path) => path.replace(/^\/warrior/, '/warrior')  // 可选：路径重写
      },
    }
  }
})
