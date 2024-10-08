<template>
  <div class="container mt-5">
    <div class="card border-0 shadow-lg p-5">
      <div class="box">
        <h3 class="text-center text-bottle-green mb-4" style="display:flex;">
          Welcome &nbsp; <strong>{{ userData.username }}</strong>
          <sup>
            <button @click="showModal" class="edit-profile-btn">
              <svg class="edit-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9"></path>
                <path d="M16.24 4.76a3 3 0 0 1 4.24 4.24L7 21H3v-4L16.24 4.76z"></path>
              </svg>
            </button>
          </sup>
        </h3>
        <div>
          <button @click="exportCampaignData" class="export-btn">
            Export Data
          </button>
        </div>
      </div>
      <p class="text-center text-light">Here is your dashboard</p>

      <!-- Display user-specific details -->
      <div v-if="userData">
        <p><strong>Email:</strong> {{ userData.email }}</p>
        <p><strong>Username:</strong> {{ userData.username }}</p>
        <p><strong>Role:</strong> {{ userData.user_type }}</p>

        <!-- Display bio information based on user type -->
        <div v-if="userData.user_type === 'influencer' && userData.influencer_bio">
          <p><strong>Name:</strong> {{ userData.influencer_bio.name }}</p>
          <p><strong>Industry:</strong> {{ userData.influencer_bio.industry }}</p>
          <p><strong>Followers:</strong> {{ userData.influencer_bio.followers }}</p>
          <p><strong>Engagement Rate:</strong> {{ userData.influencer_bio.engagement_rate }}</p>
        </div>
      </div>
      <!-- Modal for editing profile -->
      <div v-if="isModalVisible" class="modal-overlay">
        <div class="modal-content">
          <div class="card custom-card">
            <div class="card-header">
              <h5 class="card-title">Update Profile</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleProfileUpdate">
                <div class="mb-3">
                  <label for="InputUsername" class="form-label">Username</label>
                  <input
                    type="text"
                    v-model="userData.username"
                    class="form-control"
                    id="InputUsername"
                  />
                </div>
                <div class="mb-3">
                  <label for="currentPassword" class="form-label">Current Password</label>
                  <input
                    type="password"
                    v-model="userData.currentPassword"
                    class="form-control"
                    id="currentPassword"
                  />
                </div>
                <div class="mb-3">
                  <label for="newPassword" class="form-label">New Password</label>
                  <input
                    type="password"
                    v-model="userData.newPassword"
                    class="form-control"
                    id="newPassword"
                  />
                </div>
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirm Password</label>
                  <input
                    type="password"
                    v-model="userData.confirmPassword"
                    class="form-control"
                    id="confirmPassword"
                  />
                </div>
                <p v-if="isErrored" class="error-text">{{ error }}</p>
                <button type="submit" class="btn btn-primary">Update</button>
                <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


  <div class="app-container">
    <!-- <NavbarComponent /> -->
    <div class="container mt-5">
    
      <RouterView />
    </div>
  </div>
</template>

<script setup>
// import NavbarComponent from '@/components/NavbarComponent.vue'

import router from '@/router';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia';
import '../assets/SponsorDashboard.css';

const userStore = useUserStore();
const { token } = storeToRefs(userStore);

const userData = ref({
  email: '',
  username: '',
  user_type: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
  influencer_bio: null,
  sponsor_bio: null
});
const error = ref('');
const isErrored = ref(false);
const isModalVisible = ref(false);

onMounted(() => {
  if (!token.value) {
    router.push({ name: 'login' });
  } else {
    getUserProfile();
  }
});

const getUserProfile = async () => {
  try {
    const response = await axios.get('http://localhost:5000/current_user', {
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });

    console.log('User profile response:', response.data); // Debugging log

    const user = response.data?.user;
    userData.value = {
      ...user,
      influencer_bio: user.user_type === 'influencer' ? user.influencer_bio : null,
      sponsor_bio: user.user_type === 'sponsor' ? user.sponsor_bio : null
    };

    console.log('User data:', userData.value); // Debugging log
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
  }
};

const exportCampaignData = async () => {
  try {
    await axios.get('http://localhost:5000/export-campaigns', {
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
    alert('Data exported successfully');
  } catch (error) {
    console.error('Failed to export data:', error);
    alert('Failed to export data. Please try again.');
  }
};

const showModal = () => {
  isModalVisible.value = true;
};

const closeModal = () => {
  isModalVisible.value = false;
};

const handleProfileUpdate = async () => {
  isErrored.value = false;
  try {
    const response = await axios.put(
      'http://localhost:5000/user',
      {
        username: userData.value.username,
        current_password: userData.value.currentPassword,
        new_password: userData.value.newPassword,
        confirm_password: userData.value.confirmPassword,
      },
      {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      }
    );

    if (response.data.message) {
      error.value = response.data.message;
      isErrored.value = true;
      return;
    }

    alert('Profile updated successfully');
    closeModal();
    getUserProfile(); // Refresh profile data after update
  } catch (err) {
    console.error('An error occurred:', err);
    error.value =
      err.response?.data?.message ||
      'An error occurred. Please try again later.';
    isErrored.value = true;
  }
};

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
