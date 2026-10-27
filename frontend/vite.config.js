import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Dev-time API routing: one entry per game service. Mirror these in proxy/nginx.conf.
const gameServices = {
  wordle: 'http://localhost:8001',
}

const proxy = Object.fromEntries(
  Object.entries(gameServices).map(([id, target]) => [
    `/api/${id}`,
    { target, changeOrigin: true, rewrite: (path) => path.replace(`/api/${id}`, '') },
  ]),
)

export default defineConfig({
  plugins: [vue()],
  server: { proxy },
})
