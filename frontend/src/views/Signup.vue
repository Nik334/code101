<template>
  <div class="signup-container">
    <div class="signup-box">
      <SignupForm />
    </div>
  </div>
</template>

<script setup>
import SignupForm from '@/components/SignupForm.vue'
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: #f8f9fa; /* Light grey background */
  margin: 0;
}

.signup-box {
  position: relative; /* Ensure positioning context for pseudo-elements */
  background: #ffffff; /* White background */
  padding: 2.5rem; /* 40px converted to rem */
  border-radius: 0.9375rem; /* 15px converted to rem */
  box-shadow: 0 0.5rem 1.25rem rgba(0, 0, 0, 0.1); /* 8px and 20px converted to rem */
  max-width: 35rem; /* Converted to rem */
  width: 100%;
}

.signup-box::before {
  content: "";
  position: absolute;
  top: -0.9375rem; /* -15px converted to rem */
  left: -0.9375rem; /* -15px converted to rem */
  right: -0.9375rem; /* -15px converted to rem */
  bottom: -0.9375rem; /* -15px converted to rem */
  background: linear-gradient(45deg, #006A4E, #000);
  border-radius: 0.9375rem; /* 15px converted to rem */
  filter: blur(0.75rem); /* 12px converted to rem */
  opacity: 0.7; /* Slightly reduced opacity for a softer gradient */
  z-index: -1;
}
</style>
