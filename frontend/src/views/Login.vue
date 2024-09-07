<template>
  <div class="login-container">
    <div class="login-box">
      <LoginForm />
    </div>
  </div>
</template>

<script setup>
import LoginForm from '@/components/LoginForm.vue';
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa; /* Light grey background */
  margin: 0;
}

.login-box {
  position: relative; /* Ensure positioning context for pseudo-elements */
  background: #ffffff; /* White background */
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  max-width: 35rem;
  width: 100%;
}

.login-box::before {
  content: "";
  position: absolute;
  top: -15px;
  left: -15px;
  right: -15px;
  bottom: -15px;
  background: linear-gradient(45deg, #006A4E, #000);
  border-radius: 15px;
  filter: blur(12px); /* Slightly increased blur for a softer effect */
  opacity: 0.7; /* Reduced opacity for a less pronounced background */
  z-index: -1;
}
</style>
