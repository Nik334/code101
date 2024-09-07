<template>
  <div class="landing-page">
    <header class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Welcome to ConnectAd</h1>
        <p class="hero-subtitle">Your gateway to the world of influencer marketing</p>
        <div class="cta-buttons">
          <button @click="learnMore" class="btn btn-primary">Learn More</button>
          <button @click="getStarted" class="btn btn-secondary">Get Started</button>
        </div>
      </div>
    </header>

    <section class="features">
      <div class="container">
        <div v-for="(feature, index) in features" :key="index" class="feature" :class="getFeatureClass(index)">
          <img :src="feature.image" :alt="feature.title" class="feature-image">
          <h2 class="feature-title">{{ feature.title }}</h2>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <footer class="footer">
      <p>&copy; 2024 ConnectAd. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const learnMore = () => {
  console.log('Learn More clicked');
};

const getStarted = () => {
  console.log('Get Started clicked');
};

const features = ref([
  {
    title: 'Feature 1',
    description: 'Discover the amazing features that make our platform unique.',
    image: 'https://via.placeholder.com/150'
  },
  {
    title: 'Feature 2',
    description: 'Connect with top influencers and maximize your campaign reach.',
    image: 'https://via.placeholder.com/150'
  },
  {
    title: 'Feature 3',
    description: 'Analyze your campaign performance with our advanced analytics tools.',
    image: 'https://via.placeholder.com/150'
  }
]);

const getFeatureClass = (index) => {
  const delay = (index + 1) * 0.5;
  return {
    'animate__animated': true,
    'animate__fadeInUp': true,
    [`animate__delay-${delay}s`]: true
  };
};
</script>

<style scoped>
.landing-page {
  font-family: Arial, sans-serif;
}

.hero {
  background: url('https://via.placeholder.com/1920x1080') no-repeat center center/cover;
  color: #fff;
  text-align: center;
  padding: 100px 0;
  position: relative;
  overflow: hidden;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 20px;
  animation: fadeIn 2s ease-in-out;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 40px;
  animation: fadeIn 2s ease-in-out 0.5s;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn {
  padding: 15px 30px;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.3s;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #5a6268;
  transform: scale(1.05);
}

.features {
  padding: 50px 0;
  text-align: center;
}

.container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 20px;
}

.feature {
  flex: 1 1 300px;
  max-width: 300px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.feature-image {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
}

.feature-title {
  font-size: 1.25rem;
  margin-top: 10px;
}

.feature-description {
  color: #555;
}

.footer {
  background-color: #f8f9fa;
  padding: 20px;
  text-align: center;
  color: #333;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate__fadeInUp {
  animation-name: fadeInUp;
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translate3d(0, 40px, 0);
  }
  100% {
    opacity: 1;
    transform: translateZ(0);
  }
}
</style>
