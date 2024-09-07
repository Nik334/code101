<template>
  <div class="container mt-5">
    <div class="card border-0 shadow-lg p-5">
      <div class="box">
        <h3 class="text-center text-bottle-green mb-4"  style="display:flex;"> Welcome &nbsp; <strong> {{ username }} </strong>
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
      <RouterView />

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
</template>

<script setup>
import router from '@/router';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';


const userStore = useUserStore();
const { token } = storeToRefs(userStore);

const username = ref('');
const userData = ref({
  username: '',
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
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });

    username.value = response.data?.user?.username;
    userData.value.username = response.data?.user?.username;
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
.container {
  max-width: 800px;
}

.card {
  border-radius: 15px;
  background-color: #f8f9fa; /* Light background color */
  color: #000; /* Text color */
}

.text-bottle-green {
  color: #006a4e; /* Bottle green color */
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
}

p {
  font-size: 1.2rem;
}

.box {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.export-btn {
  border: solid 1px #006a4e; /* Bottle green border */
  border-radius: 5px;
  background-color: white;
  padding: 10px 15px;
  color: #006a4e; /* Bottle green text */
  outline: none;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.export-btn:hover {
  background-color: #006a4e;
  color: white;
}

.edit-profile-btn {
  border: none;
  background-color: transparent;
  color: #006a4e; /* Bottle green color */
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 1rem;
  padding: 10px 15px;
  transition: color 0.3s;
}

.edit-profile-btn:hover {
  color: #004a39; /* Darker bottle green */
}

.edit-icon {
  margin-right: 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
}

/* Custom styles for the profile update card */
.card.custom-card {
  background-color: #006a4e; /* Bottle green background color */
  border: 2px solid black; /* Black border */
  color: white; /* Ensure text is readable */
}

.card-header {
  text-align: center;
  margin-bottom: 1rem;
}

.card-header .card-title {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.card.custom-card .form-control,
.card.custom-card .form-select {
  background-color: white; /* Keep input fields white */
  color: black; /* Black text color in input fields */
}

.card.custom-card .form-label {
  color: white; /* White text for labels */
}

.card.custom-card .btn-primary {
  background-color: black; /* Black button background */
  border-color: black; /* Black button border */
}

.card.custom-card .btn-primary:hover {
  background-color: #333; /* Darker shade for hover */
}

.error-text {
  color: red; /* Error text styling */
}
</style>
