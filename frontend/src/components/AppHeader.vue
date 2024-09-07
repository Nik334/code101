<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-light bg-dark">
      <a class="navbar-brand" href="/sponsor-dashboard">
        <img alt="Vue logo" src="@/assets/logo.svg" width="50" height="50" class="ms-5"/>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li v-if="isAuthenticated" class="nav-item">
            <RouterLink class="nav-link" to="/sponsor-dashboard">Sponsor Dashboard</RouterLink>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <RouterLink class="nav-link" to="/influencer-dashboard">Influencer Dashboard</RouterLink>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <RouterLink class="nav-link" to="/admin-dashboard">Admin Dashboard</RouterLink>
          </li>
          <li v-if="!isAuthenticated" class="nav-item">
            <RouterLink class="nav-link" to="/signup">Signup</RouterLink>
          </li>
          <li v-if="!isAuthenticated" class="nav-item">
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <button @click="logout" class="nav-link btn btn-link">Logout</button>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = ref(false);

onMounted(() => {
  isAuthenticated.value = Boolean(localStorage.getItem('userId')); // Check authentication
});

const logout = () => {
  localStorage.removeItem('userId'); // Clear authentication
  isAuthenticated.value = false;
  router.push('/login'); // Redirect to login
};
</script>

<style scoped>
.nav-link {
  color: #007bff;
  transition: color 0.3s ease, background-color 0.3s ease;
}

.nav-link:hover {
  color: #fff;
  background-color: #007bff;
  text-decoration: none;
  border-radius: 4px;
}

.nav-link {
  padding: 0.5rem 2rem;
  margin: 1rem;
}
</style>
