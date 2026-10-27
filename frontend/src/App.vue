<template>
  <header class="site-header">
    <RouterLink to="/" class="brand">MindGames</RouterLink>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style>
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #fafafa;
  color: #222;
}
.site-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #ddd;
  background: #fff;
}
.brand {
  font-weight: 700;
  font-size: 1.25rem;
  color: inherit;
  text-decoration: none;
}
main {
  padding: 1.5rem;
  max-width: 960px;
  margin: 0 auto;
}
</style>
