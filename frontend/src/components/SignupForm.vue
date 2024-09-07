<template>
  <div class="card custom-card">
    <div class="card-header">ConnectAd</div>
    <div class="card-body">
      <h5 class="card-title">Create an Account</h5>
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
          <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
        </div>
        <div class="mb-3">
          <label for="InputName" class="form-label">Name</label>
          <input type="text" v-model="name" class="form-control" id="InputName" />
        </div>
        <div class="mb-3">
          <label for="InputUsername" class="form-label">Username</label>
          <input type="text" v-model="username" class="form-control" id="InputUsername" />
        </div>
        <div class="mb-3">
          <label for="InputPassword1" class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" id="InputPassword1" />
        </div>
        <div class="mb-3">
          <label for="InputRole" class="form-label">Role</label>
          <select class="form-select" v-model="user_role" id="InputRole" aria-label="user type">
            <option selected>Select Role</option>
            <option value="sponsor">Sponsor</option>
            <option value="influencer">Influencer</option>
          </select>
        </div>
        <template v-if="user_role === 'sponsor'">
          <div class="mb-3">
            <label for="InputIndustry" class="form-label">Industry</label>
            <input type="text" v-model="industry" class="form-control" id="InputIndustry" />
          </div>
          <div class="mb-3">
            <label for="InputBudget" class="form-label">Budget</label>
            <input type="number" v-model="budget" class="form-control" id="InputBudget" />
          </div>
        </template>
        <template v-if="user_role === 'influencer'">
          <div class="mb-3">
            <label for="category" class="form-label">Category</label>
            <input type="text" v-model="category" class="form-control" id="category" />
          </div>
          <div class="mb-3">
            <label for="niche" class="form-label">Niche</label>
            <input type="text" v-model="niche" class="form-control" id="niche" />
          </div>
        </template>
        <button type="submit" class="btn btn-primary">Register</button>
        <p>Already have an account? <router-link to="/login">Login</router-link></p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const email = ref('')
const name = ref('')
const username = ref('')
const password = ref('')
const user_role = ref('')
const industry = ref('')
const budget = ref('')
const category = ref('')
const niche = ref('')

const userStore = useUserStore()
const router = useRouter()

const { setToken, setUsername, setRole } = userStore

const handleSubmit = async () => {
  try {
    let response
    if (user_role.value === 'sponsor') {
      response = await axios.post('http://localhost:5000/signup', {
        email: email.value,
        name: name.value,
        username: username.value,
        password: password.value,
        user_type: user_role.value,
        budget: budget.value,
        industry: industry.value
      })
    } else if (user_role.value === 'influencer') {
      response = await axios.post('http://localhost:5000/signup', {
        email: email.value,
        name: name.value,
        username: username.value,
        password: password.value,
        user_type: user_role.value,
        category: category.value,
        niche: niche.value
      })
    }

    console.log('Response data:', response.data)

    // Assuming the response contains token, user, and user_type
    sessionStorage.setItem('token', response.data.token)
    sessionStorage.setItem('user', JSON.stringify(response.data.user))
    sessionStorage.setItem('user_type', response.data.user_type)

    setToken(response.data.token)
    setUsername(response.data.user)
    setRole(response.data.user_type)

    router.push('/login') // Redirect to login page after successful registration
  } catch (error) {
    console.error('An error occurred:', error)
  }
}
</script>

<style scoped>
.card.custom-card {
  background-color: #006a4e; /* Bottle green background color */
  border: 2px solid black; /* Black border */
  color: white; /* Ensure text is readable */
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
</style>
