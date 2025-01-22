import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    server: {
        port: 8080,
        cors: true,
        headers: {
            'Access-Control-Allow-Origin': 'http://localhost:8000',
        },
    },
    resolve: {
        alias: {
            '@': '/src',
        },
    },
})