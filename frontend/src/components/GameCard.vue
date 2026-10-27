<script setup>
defineProps({
  game: { type: Object, required: true },
})
</script>

<template>
  <RouterLink :to="`/games/${game.id}`" class="card">
    <h2>{{ game.name }}</h2>
    <p>{{ game.description }}</p>
  </RouterLink>
</template>

<style scoped>
.card {
  display: block;
  padding: 1rem 1.25rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  color: inherit;
  text-decoration: none;
}
.card:hover {
  border-color: #888;
}
h2 {
  margin: 0 0 0.5rem;
}
p {
  margin: 0;
  color: #555;
}
</style>
