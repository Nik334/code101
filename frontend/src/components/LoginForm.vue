<template>
  <div class="card custom-card">
    <div class="card-header">
      <h1 class="card-title">ConnectAd</h1>
      <p class="card-subtitle">Catalyze communication with the right connections</p>
    </div>
    <div class="card-body">
      <h5 class="card-title">Login</h5>
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="InputEmail1" class="form-label">Email address</label>
          <input
            type="email"
            v-model="email"
            class="form-control"
            id="InputEmail1"
            aria-describedby="emailHelp"
          />
        </div>
        <div class="mb-3">
          <label for="InputPassword1" class="form-label">Password</label>
          <input
            type="password"
            v-model="password"
            class="form-control"
            id="InputPassword1"
          />
        </div>
        <p v-if="isErrored" class="error-text">{{ error }}</p>
        <button type="submit" class="btn btn-primary">Login</button>
        <p>Don't have an account? <router-link to="/signup">Sign up</router-link></p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref('');
const isErrored = ref(false);

const userStore = useUserStore();
const router = useRouter();

const handleSubmit = async () => {
  isErrored.value = false;
  try {
    // Perform the login request
    const response = await axios.post('http://localhost:5000/login', {
      email: email.value,
      password: password.value
    });

    // Handle errors in the response
    if (response.data.error) {
      error.value = response.data.error;
      isErrored.value = true;
      return;
    }

    // Retrieve and store data from the response
    const { token, user, user_type } = response.data;

    // Set local storage
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('user_type', user_type);

    // Update user store
    userStore.setToken(token);
    userStore.setUsername(user.username); // Adjust based on your API response
    userStore.setRole(user_type);

    // Redirect based on user type
    switch (user_type) {
      case 'sponsor':
        router.push('/sponsor-dashboard/profile');
        break;
      case 'influencer':
        router.push('/influencer-dashboard/profile');
        break;
      default:
        router.push('/admin-dashboard');
        break;
    }
  } catch (err) {
    // Handle errors that occur during the request
    console.error('An error occurred:', err);
    error.value = err.response?.data?.message || 'An error occurred. Please try again later.';
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
