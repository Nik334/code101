<template>
  <div class="full-screen-container">
    <div class="content-container">
      <h1 class="text-bottle-green">Welcome, {{ username }}</h1>
      <h3 class="my-4 text-black">Ongoing Campaigns</h3>
      <div v-if="campaigns.length === 0">
        <div class="alert alert-warning" role="alert">No ongoing campaigns.</div>
      </div>
      <div class="campaign-grid">
        <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-card-wrapper">
          <CampaignCard
            :campaign="campaign"
            @request-campaign="fetchall"
            :admin="true"
            :flagged="false"
          />
        </div>
      </div>

      <h3 class="my-4 text-black">Flagged Campaigns</h3>
      <div v-if="flaggedCampaigns.length === 0">
        <div class="alert alert-danger" role="alert">No flagged campaigns.</div>
      </div>
      <div class="campaign-grid">
        <div v-for="campaign in flaggedCampaigns" :key="campaign.id" class="campaign-card-wrapper">
          <CampaignCard
            :campaign="campaign"
            @request-campaign="fetchall"
            :admin="true"
            :flagged="true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import CampaignCard from '@/components/AdminCampaignCard.vue'
import NavbarComponent from '@/components/NavbarComponent.vue'
import router from '@/router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

// Access the user store
const userStore = useUserStore()
const { token, username } = storeToRefs(userStore)

const campaigns = ref([])
const flaggedCampaigns = ref([])

const fetchall = async () => {
  await fetchFlaggedCampaigns()
  await fetchCampaigns()
}

const fetchFlaggedCampaigns = async () => {
  try {
    const response = await axios.get('http://localhost:5000/flagged-campaigns', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    flaggedCampaigns.value = response.data
  } catch (error) {
    console.error('Failed to fetch flagged campaigns:', error)
  }
}

const fetchCampaigns = async () => {
  try {
    const response = await axios.get('http://localhost:5000/unflag-campaigns', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    campaigns.value = response.data
  } catch (error) {
    console.error('Failed to fetch ongoing campaigns:', error)
  }
}

onMounted(() => {
  if (!token.value) {
    router.push({ name: 'login' })
  } else {
    // Log the token value for debugging purposes
    console.log(`Token: ${token.value}`)

    // Fetch data if token is present
    fetchCampaigns()
    fetchFlaggedCampaigns()
  }
})
</script>

<style scoped>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

body {
  width: 100%;
  margin: 0;
}

.full-screen-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-container {
  flex: 1;
  padding: 2rem;
  background-color: #f8f9fa;
}

.text-bottle-green {
  color: #006a4e;
}

.bg-bottle-green {
  background-color: #006a4e;
}

.border-bottle-green {
  border-color: #006a4e;
}

.campaign-card {
  transition: transform 0.3s ease;
}

.campaign-card:hover {
  transform: scale(1.05);
}

.campaign-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.campaign-card-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>