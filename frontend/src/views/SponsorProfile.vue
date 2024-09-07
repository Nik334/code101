<template>
  <div class="container mt-5">
    <h1 class="mb-4 text-center text-bottle-green">Active Campaigns</h1>
    <div v-if="campaigns.length === 0" class="text-center">
      <p class="text-muted">No active campaigns.</p>
    </div>
    <div class="row justify-content-center">
      <div v-for="campaign in campaigns" :key="campaign.id" class="col-md-4 mb-4">
        <div class="card text-center campaign-card">
          <div class="card-header box">
            <p>{{ campaign.campaign_visibility }}</p>
            <button @click="deleteCampaign(campaign.id)">Delete</button>
          </div>
          <div class="card-body">
            <h5 class="card-title">
              {{ campaign.campaign_name }} - INR {{ campaign.campaign_budget }}
            </h5>
            <p class="card-text">
              {{ campaign.campaign_desc }}
            </p>
            <!-- Uncomment this line if you decide to add a "Create Ad Request" button -->
            <!-- <a href="#" class="btn btn-outline-bottle-green">Create Ad Request</a> -->
          </div>
          <div class="card-footer">
            {{ campaign.campaign_start }} - {{ campaign.campaign_end }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'
import router from '@/router'

const userStore = useUserStore()
const { token } = storeToRefs(userStore)

const campaigns = ref([])

const fetchMyActiveCampaigns = async () => {
  try {
    const response = await axios.get('http://localhost:5000/active-campaigns', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    campaigns.value = response.data
  } catch (error) {
    console.error('Error fetching campaigns:', error)
  }
}

const deleteCampaign = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/campaigns/${id}`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    await fetchMyActiveCampaigns()
  } catch (error) {
    console.error('Error deleting campaign:', error)
  }
}

onMounted(() => {
  if (!token.value) {
    router.push({ name: 'login' })
  } else {
    fetchMyActiveCampaigns()
  }
})
</script>
<style scoped>
.container {
  max-width: 1200px;
  margin: auto;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #006a4e; /* Bottle green */
  margin-bottom: 1.5rem;
}

.text-muted {
  color: #6c757d;
}

.card {
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* Smooth transition */
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Enhanced shadow on hover */
  transform: translateY(-5px); /* Lift effect on hover */
}

.card-header {
  background: linear-gradient(135deg, #006a4e 0%, #004d40 100%); /* Gradient background */
  color: #fff;
  padding: 1rem;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-footer {
  background: #f8f9fa;
  color: #343a40;
  font-size: 0.9rem;
  padding: 0.75rem;
  border-top: 1px solid #e9ecef;
}

.card-body {
  padding: 1.5rem;
  background-color: #fff;
  color: #343a40;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.card-text {
  font-size: 1rem;
  margin-bottom: 1rem;
}

.box {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box button {
  border: 2px solid #dc3545; /* Red border */
  border-radius: 5px;
  background-color: #fff;
  color: #dc3545; /* Red text */
  padding: 0.5rem 1rem;
  outline: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.box button:hover {
  background-color: #dc3545;
  color: #fff;
}

.btn-outline-bottle-green {
  color: #006a4e;
  border-color: #006a4e;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  font-weight: 500;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-outline-bottle-green:hover {
  background-color: #006a4e;
  color: #fff;
}

.text-center {
  text-align: center;
}

</style>
