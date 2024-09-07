<template>
  <div class="container my-5">
    <div v-if="campaigns.length === 0" class="text-center">
      <h2 class="text-black mb-4">No campaigns found</h2>
      <p class="lead text-muted">Time to start!</p>
    </div>
    <div v-else>
      <h2 class="text-bottle-green mb-4">All Campaigns</h2>
      <input
        class="form-control mb-4"
        type="search"
        placeholder="Search"
        aria-label="Search"
        v-model="searchQuery"
      />
      <div class="row">
        <div v-for="campaign in searchedCampaigns" :key="campaign.id" class="col-md-6 mb-4">
          <CampaignCard :campaign="campaign" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'
import router from '@/router'
import CampaignCard from '@/components/CampaignCard.vue'

const userStore = useUserStore()
const { token } = storeToRefs(userStore)

const campaigns = ref([])
const searchQuery = ref('')

const searchedCampaigns = computed(() => {
  return campaigns.value.filter((campaign) => {
    return campaign.campaign_name.toLowerCase().indexOf(searchQuery.value.toLowerCase()) !== -1
  })
})

const fetchPublicCampaigns = async () => {
  await axios
    .get('http://localhost:5000/public-campaigns', {
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

onMounted(() => {
  if (!token) {
    router.push({ name: 'login' })
  }
  fetchPublicCampaigns()
})
</script>

<style scoped>
.text-bottle-green {
  color: #006A4E;
}

.text-black {
  color: #000;
}

.lead {
  font-size: 1.25rem;
  font-weight: 300;
}
</style>
