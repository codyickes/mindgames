// Game registry: add one entry per game. Router and Home page are built from this list.
export default [
  {
    id: 'wordle',
    name: 'Wordle',
    description: 'Guess the five-letter word in six tries.',
    component: () => import('./wordle/WordleGame.vue'),
  },
]
