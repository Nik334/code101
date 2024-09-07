<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">ConnectAd</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav ms-auto">
            <template v-if="!isAuthenticated">
              <!-- Show these links only when the user is not authenticated -->
              <a class="nav-link" href="/login">Login</a>
              <a class="nav-link" href="/signup">Signup</a>
            </template>

            <template v-if="isAuthenticated">
              <!-- Show these links only when the user is authenticated -->
              <template v-if="userRole === 'influencer'">
                <a class="nav-link" aria-current="page" :href="influencerProfileUrl">Profile</a>
                <a class="nav-link" :href="influencerCampaignsUrl">Find Campaigns</a>
                <button class="nav-link btn btn-link" @click="logoutUser">Logout</button>
              </template>

              <template v-if="userRole === 'sponsor'">
                <a class="nav-link" aria-current="page" :href="sponsorProfileUrl">Profile</a>
                <a class="nav-link" :href="sponsorCampaignsUrl">My Campaigns</a>
                <button class="nav-link btn btn-link" @click="logoutUser">Logout</button>
              </template>

              <template v-if="userRole === 'admin'">
                <a class="nav-link" :href="adminDashboardUrl">Admin Dashboard</a>
                <button class="nav-link btn btn-link" @click="logoutUser">Logout</button>
              </template>
            </template>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const router = useRouter();

// Computed properties to derive state from Pinia store
const isAuthenticated = computed(() => !!userStore.token);
const userRole = computed(() => userStore.role);

// Define URLs for navigation dynamically
const influencerProfileUrl = '/influencer-dashboard/profile';
const influencerCampaignsUrl = '/influencer-dashboard/campaigns';
const sponsorProfileUrl = '/sponsor-dashboard/profile';
const sponsorCampaignsUrl = '/sponsor-dashboard/campaigns';
const adminDashboardUrl = '/admin-dashboard';

const logoutUser = () => {
  userStore.logout(); // Call the store method to clear state
  router.push('/login');
};
</script>
<style scoped>
.nav-link {
  color: #006a4e; /* Bootstrap primary color */
  transition: color 0.3s ease, background-color 0.3s ease, transform 0.3s ease;
}

.nav-link:hover {
  color: #fff;
  background-color: #006a4e;
  text-decoration: none;
  border-radius: 4px;
  transform: scale(1.1); /* Slightly increase size on hover */
}

.navbar-nav .nav-link {
  margin-right: 1rem; /* Gap between nav items */
}

.navbar-nav .nav-link:last-child {
  margin-right: 0; /* Remove gap for the last item */
}

.nav-link {
  padding: 0.5rem 1rem; /* Adjusted padding */
}

.navbar-nav {
  margin-left: auto; /* Pushes the items to the right */
}

.navbar-toggler {
  border: none;
}

.container-fluid {
  padding: 0;
}

.navbar {
  padding: 0.5rem 1rem; /* Adjusted padding for the navbar */
}
</style>
