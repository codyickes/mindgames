<script setup>
import games from '../games'
import GameCard from '../components/GameCard.vue'
</script>

<template>
  <h1>Pick a game</h1>
  <div class="grid">
    <GameCard v-for="game in games" :key="game.id" :game="game" />
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}
</style>
