<template>
  <div class="card custom-card">
    <div class="card-header">
      <h5 class="card-title">Update Profile</h5>
    </div>
    <div class="card-body">
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="InputUsername" class="form-label">Username</label>
          <input
            type="text"
            v-model="username"
            class="form-control"
            id="InputUsername"
          />
        </div>
        <div class="mb-3">
          <label for="currentPassword" class="form-label"
            >Current Password</label
          >
          <input
            type="password"
            v-model="currentPassword"
            class="form-control"
            id="currentPassword"
          />
        </div>
        <div class="mb-3">
          <label for="newPassword" class="form-label">New Password</label>
          <input
            type="password"
            v-model="newPassword"
            class="form-control"
            id="newPassword"
          />
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="form-label"
            >Confirm Password</label
          >
          <input
            type="password"
            v-model="confirmPassword"
            class="form-control"
            id="confirmPassword"
          />
        </div>
        <p v-if="isErrored" class="error-text">{{ error }}</p>
        <button type="submit" class="btn btn-primary">Update</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { token } = storeToRefs(userStore)

const username = ref('');
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const error = ref('');
const isErrored = ref(false);

const handleSubmit = async () => {
  isErrored.value = false;
  try {
    // Perform the login request
    const response = await axios.put(
      'http://localhost:5000/user',
      {
        username: username.value,
        current_password: currentPassword.value,
        new_password: newPassword.value,
        confirm_password: confirmPassword.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      }
    );

    // Handle errors in the response
    if (response.data.error) {
      error.value = response.data.error;
      isErrored.value = true;
      return;
    }
  } catch (err) {
    // Handle errors that occur during the request
    console.error('An error occurred:', err);
    error.value =
      err.response?.data?.message ||
      'An error occurred. Please try again later.';
    isErrored.value = true;
  }
};
</script>

<style scoped>
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

.card-header .card-subtitle {
  font-size: 0.9rem;
  color: #d3d3d3; /* Lighter color for subtitle */
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

.card {
  width: 30rem;
  margin: 0 auto;
}

.error-text {
  color: red; /* Error text styling */
}
</style>
