<template>
  <div class="app-container">
    <!-- <NavbarComponent /> -->
    <div class="container mt-5">
      <h1 class="text-bottle-green mb-4">Welcome, {{ username }}</h1>
      <RouterView />
    </div>
  </div>
</template>

<script setup>
// import NavbarComponent from '@/components/NavbarComponent.vue'
import router from '@/router'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'

const username = localStorage.getItem('username')

const userStore = useUserStore()
const { token } = storeToRefs(userStore)

onMounted(() => {
  if (!token) {
    router.push({ name: 'login' })
  }
})
</script>

<style lang="scss" scoped>
.app-container {
  background-color: #f8f9fa; /* Light grey background for contrast */
  min-height: 100vh; /* Ensure the app takes up the full viewport height */
  padding-bottom: 20px; /* Space at the bottom for better aesthetics */
}

.text-bottle-green {
  color: #006A4E;
  font-weight: bold;
}

.container {
  background: #ffffff; /* White background for the main content area */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}
</style>
