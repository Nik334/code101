<template>
  <div class="campaign-container">
    <button
      v-if="campaigns.length !== 0"
      class="btn btn-primary add-campaign-btn"
      type="button"
      data-bs-toggle="offcanvas"
      data-bs-target="#offcanvasExample"
      aria-controls="offcanvasExample"
    >
      Add Campaign
    </button>

    <div
      class="offcanvas offcanvas-start"
      tabindex="-1"
      id="offcanvasExample"
      aria-labelledby="offcanvasExampleLabel"
    >
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasExampleLabel">Create a Campaign</h5>
        <button
          type="button"
          class="btn-close text-reset"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body">
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="title" class="form-label">Campaign Title</label>
            <input
              type="text"
              v-model="title"
              class="form-control"
              id="title"
              aria-describedby="title"
            />
          </div>

          <div class="mb-3">
            <label for="description" class="form-label">Campaign Description</label>
            <textarea
              v-model="description"
              class="form-control"
              id="description"
              rows="3"
            ></textarea>
          </div>

          <div class="mb-3">
            <label for="budget" class="form-label">Campaign Budget</label>
            <input
              type="number"
              v-model="budget"
              class="form-control"
              id="budget"
              aria-describedby="budget"
              min="0"
            />
          </div>

          <div class="d-flex justify-content-between">
           <div class="mb-3">
            <label for="startDate">Start Date</label>
            <input
              type="date"
              v-model="startDate"
              class="form-control"
              id="startDate"
              :min="today"
              aria-describedby="startDate"
            />
            <div v-if="startDateError" class="text-danger">{{ startDateError }}</div>
          </div>
            <div class="mb-3">
              <label for="endDate">End Date</label>
              <input
                type="date"
                v-model="endDate"
                class="form-control"
                id="endDate"
                :min="startDate"
                aria-describedby="endDate"
              />
              <div v-if="endDateError" class="text-danger">{{ endDateError }}</div>
            </div>
          </div>

          <div class="mb-3 form-check form-switch">
            <label class="form-check-label" for="flexSwitchCheckDefault">Set as public</label>
            <input
              class="form-check-input"
              type="checkbox"
              v-model="visibility"
              id="flexSwitchCheckDefault"
            />
          </div>
           <div v-if="!visibility" class="mb-3">
            <label for="influencer" class="form-label">Select Influencer</label>
            <select
              v-model="selectedInfluencer"
              class="form-control"
              id="influencer"
            >
              <option disabled value="">Select an Influencer</option>
          <option v-for="influencer in influencers" :key="influencer.id" :value="influencer.id">
  {{ influencer.name }}
</option>

            </select>
          </div>

          <div class="mb-3">
            <label for="goal" class="form-label">Campaign Goal</label>
            <input
              type="text"
              v-model="goal"
              class="form-control"
              id="goal"
              aria-describedby="goal"
            />
          </div>

          <button
            type="submit"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
            class="btn btn-primary"
            :disabled="startDateError || endDateError"
          >
            Create Campaign
          </button>
        </form>
      </div>
    </div>

    <div v-if="campaigns.length === 0">
      <h2>No campaigns found</h2>
      <button
        class="btn btn-primary add-campaign-btn"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasExample"
        aria-controls="offcanvasExample"
      >
        Add Campaign
      </button>
    </div>

    <div v-else>
      <h2 style="margin-bottom: 2.5rem">My Campaigns</h2>
      <div v-for="campaign in campaigns" :key="campaign.id">
        <CampaignCard :campaign="campaign" @campaign-fetch="fetchMyCampaigns" />
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
import CampaignCard from '@/components/CampaignCard.vue'

const userStore = useUserStore()
const { token } = storeToRefs(userStore)

const title = ref('')
const description = ref('')
const budget = ref('')
const startDate = ref('')
const endDate = ref('')
const influencers = ref('')
const visibility = ref(false)
const goal = ref('')

const campaigns = ref([])
console.log("influencers for id check ",influencers.value)

const today = computed(() => {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
})
const startDateError = ref('')
const endDateError = ref('')

watch([startDate, endDate], ([newStartDate, newEndDate]) => {
  startDateError.value = ''
  endDateError.value = ''
  
  if (newStartDate && newEndDate && newEndDate < newStartDate) {
    endDateError.value = 'End date must be after the start date.'
  }
})

const handleSubmit = async () => {
  try {
    await axios.post(
      'http://localhost:5000/create-campaign',
      {
        name: title.value,
        description: description.value,
        budget: budget.value,
        start_date: startDate.value,
        end_date: endDate.value,
        visibility: visibility.value ? 'public' : 'private',
        goal: goal.value,
        influencer_id: !visibility.value ? influencer.value : null
      },
      {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      }
    )
    fetchMyCampaigns()
    console.log("influencer_id",influencer_id)
    console.log("influencer_id c", influencers.value)

  } catch (error) {
    console.error('Failed to create campaign:', error)
  }
}

const fetchMyCampaigns = async () => {
  console.log("fetchMyCampign");
  try {
    const response = await axios.get('http://localhost:5000/my-campaigns', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    campaigns.value = response.data
  } catch (error) {
    console.error('Failed to fetch campaigns:', error)
  }
}


const fetchInfluencers = async () => {
  try {
    const response = await axios.get('http://localhost:5000/influencers', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    influencers.value = response.data
  } catch (error) {
    console.error('Failed to fetch influencers:', error)
  }
}

onMounted(() => {
  if (!token.value) {
    router.push({ name: 'login' })
  } else {
    fetchMyCampaigns()
    fetchInfluencers()
  }
})
</script>

<style scoped>
.campaign-container {
  padding: 1rem; /* 16px / 16 = 1rem */
  background-color: #f8f9fa;
}

.add-campaign-btn {
  background-color: #006a4e;
  border: none;
  color: white;
  font-weight: bold;
  box-shadow: 0 0.25rem 0.9375rem rgba(0, 106, 78, 0.5); /* 4px 15px */
  transition: transform 0.2s;
}

.add-campaign-btn:hover {
  transform: scale(1.05);
  background-color: #004d3a;
}

.offcanvas-header {
  background-color: #006a4e;
  color: white;
}

.offcanvas-body {
  background-color: #ffffff;
  padding: 1.25rem; /* 20px / 16 = 1.25rem */
  border-radius: 0.9375rem; /* 15px / 16 = 0.9375rem */
  box-shadow: 0 0.5rem 1.25rem rgba(0, 0, 0, 0.1); /* 8px 20px */
}

.form-control {
  border-radius: 0.625rem; /* 10px / 16 = 0.625rem */
}

.btn-primary {
  background-color: #006a4e;
  border: none;
  box-shadow: 0 0.25rem 0.625rem rgba(0, 106, 78, 0.3); /* 4px 10px */
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #004d3a;
}
</style>
