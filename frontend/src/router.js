import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import games from './games'

const routes = [
  { path: '/', component: Home },
  ...games.map((game) => ({
    path: `/games/${game.id}`,
    component: game.component,
    meta: { title: game.name },
  })),
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({ history: createWebHistory(), routes })

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} · MindGames` : 'MindGames'
})

export default router
