<template>
  <div class="container my-5">
    <div class="mb-5">
      <h1 class="text-bottle-green mb-4">Active Campaigns</h1>
      <div v-if="campaigns.length !== 0">
        <div class="row">
          <div v-for="campaign in campaigns" :key="campaign.id" class="col-md-6 mb-4">
            <div class="card text-center campaign-card border-bottle-green">
              <div class="card-header bg-bottle-green text-white">{{ campaign.campaign_visibility }}</div>
              <div class="card-body">
                <h5 class="card-title text-black">
                  {{ campaign.campaign_name }} - INR {{ campaign.campaign_budget }}
                </h5>
                <p class="card-text text-muted">
                  {{ campaign.campaign_desc }}
                </p>
              </div>
              <div class="card-footer text-muted">
                {{ campaign.campaign_start }} - {{ campaign.campaign_end }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center">
        <h3 class="text-muted">No Active Campaigns</h3>
      </div>
    </div>

    <div>
      <h1 class="text-bottle-green mb-4">Incoming Requests</h1>
      <div v-if="incomingRequests.length !== 0">
        <div class="row">
          <div v-for="ad in incomingRequests" :key="ad.id" class="col-md-6 mb-4">
            <IncomingRequestCard
              :ad="ad"
              @request-accepted="fetchMyActiveCampaigns"
              @refresh-requests="fetchIncomingRequests"
            />
          </div>
        </div>
      </div>
      <div v-else class="text-center">
        <h3 class="text-muted">No Incoming Requests</h3>
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
import IncomingRequestCard from '@/components/IncomingRequestCard.vue'

const userStore = useUserStore()
const { token } = storeToRefs(userStore)

const campaigns = ref([])
const incomingRequests = ref([])

const fetchMyActiveCampaigns = async () => {
  await axios
    .get('http://localhost:5000/influencer-active-campaigns', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then((response) => {
      campaigns.value = response.data
    })
    .catch((error) => {
      console.error(error)
    })
}

const fetchIncomingRequests = async () => {
  await axios
    .get('http://localhost:5000/get-pending-ads', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then((response) => {
      incomingRequests.value = response.data
    })
    .catch((error) => {
      console.error(error)
    })
}

onMounted(() => {
  if (!token) {
    router.push({ name: 'login' })
  }
  fetchMyActiveCampaigns()
  fetchIncomingRequests()
})
</script>

<style scoped>
.text-bottle-green {
  color: #006A4E;
}

.campaign-card {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.campaign-card:hover {
  transform: translateY(-10px);
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
}

.bg-bottle-green {
  background-color: #006A4E;
}

.border-bottle-green {
  border-color: #006A4E;
}

.text-black {
  color: #000;
}

.text-muted {
  color: #6c757d;
}
</style>
