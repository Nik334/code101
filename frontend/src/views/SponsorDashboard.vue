<template>
  <div class="container mt-5">
    <div class="card border-0 shadow-lg p-4 p-md-5">
      <!-- Welcome Section -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class=" text-bottle-green mb-0">
          Welcome, <strong>{{ userData.username }}</strong>
        </h3>
        <button @click="showModal" class="edit-profile-btn">
          <svg class="edit-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"></path>
            <path d="M16.24 4.76a3 3 0 0 1 4.24 4.24L7 21H3v-4L16.24 4.76z"></path>
          </svg>
        </button>
      </div>

      <!-- User Information Card -->
      <div v-if="userData" class="card mb-4">
        <div class="card-body">
          <div class="user-info">
            <div class="info-item">
              <i class="fa fa-envelope info-icon"></i>
              <p><strong>Email:</strong> {{ userData.email }}</p>
            </div>
            <div class="info-item">
              <i class="fa fa-user info-icon"></i>
              <p><strong>Role:</strong> {{ userData.user_type }}</p>
            </div>
            <!-- Display Sponsor Bio -->
            <div v-if="userData.user_type === 'sponsor' && userData.sponsor_bio" class="bio-info">
              <div class="info-item">
                <i class="fa fa-id-card info-icon"></i>
                <p><strong>Name:</strong> {{ userData.sponsor_bio.name }}</p>
              </div>
              <div class="info-item">
                <i class="fa fa-industry info-icon"></i>
                <p><strong>Industry:</strong> {{ userData.sponsor_bio.industry }}</p>
              </div>
              <div class="info-item">
                <i class="fa fa-dollar-sign info-icon"></i>
                <p><strong>Budget:</strong> {{ userData.sponsor_bio.budget }}</p>
              </div>
              <div class="info-item">
                <i class="fa fa-check-circle info-icon"></i>
                <p><strong>Approved:</strong> {{ userData.sponsor_bio.approved ? 'Yes' : 'No' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="text-right">
        <button @click="exportCampaignData" class="export-btn">
          Export Data
        </button>
      </div>
    </div>
    <RouterView />

    <!-- Modal for Editing Profile -->
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
              <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-primary">Update</button>
                <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import '../assets/SponsorDashboard.css';

const router = useRouter();
const userStore = useUserStore();
const { token } = storeToRefs(userStore);

const userData = ref({
  username: '',
  email: '',
  user_type: '',
  sponsor_bio: null,
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
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
      headers: { Authorization: `Bearer ${token.value}` }
    });

    const user = response.data?.user;
    userData.value = {
      ...user,
      sponsor_bio: user.user_type === 'sponsor' ? user.sponsor_bio : null
    };
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
  }
};

const exportCampaignData = async () => {
  try {
    await axios.get('http://localhost:5000/export-campaigns', {
      headers: { Authorization: `Bearer ${token.value}` }
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
        confirm_password: userData.value.confirmPassword
      },
      {
        headers: { Authorization: `Bearer ${token.value}` }
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
    error.value = err.response?.data?.message || 'An error occurred. Please try again later.';
    isErrored.value = true;
  }
};
</script>
