<template>
  <div id="app">
    <!-- Include the header component here -->
    <!-- <AppHeader /> -->
    <NavbarComponent/>
    
    <!-- Main content of the application rendered by Vue Router -->
    <RouterView />
  </div>
</template>

<script setup>
// import AppHeader from '@/components/AppHeader.vue';
import NavbarComponent from '@/components/NavbarComponent.vue';
import { RouterView } from 'vue-router';
</script>

<style>
/* Global styles for your app */
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  color: #333;
  background-color: #f8f9fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

body {
  margin: 0;
  padding: 0;
}

a {
  text-decoration: none;
}

nav {
  margin-bottom: 2rem;
}
</style>
