<template>
  <div class="card campaign-card m-1">
    <header class="card-header bg-bottle-green">
      <div class="visibility-icon">
        <PublicIcon v-if="campaign.campaign_visibility === 'public'" />
        <PrivateIcon v-else />
      </div>
      <p class="visibility-label">
        <strong>Visibility:</strong> {{ campaign.campaign_visibility }}
      </p>
      <div>
        <button @click="openEditModal" class="btn btn-primary m-2">
          <PencilSharp class="edit-icon" />
        </button>
        <button @click="deleteCampaign(campaign.id)" class="btn btn-danger">
          <TrashOutline class="delete-icon" />
        </button>
      </div>
    </header>
    <main class="card-body">
      <h5 class="card-title">
        <strong>Campaign Title: {{ campaign.campaign_name }} - INR {{ campaign.campaign_budget }}</strong>
      </h5>
      <p class="card-text">
        <strong>Description:</strong> {{ campaign.campaign_desc }}
      </p>
    </main>
    <footer class="card-footer">
      <div>
        <strong>Start Date:</strong> {{ formatDate(campaign.campaign_start) }}
        <strong>End Date:</strong> {{ formatDate(campaign.campaign_end) }}
      </div>
    </footer>

    <!-- Edit Modal -->
    <transition name="fade">
      <div v-if="open" class="modal-overlay" @click.self="closeEditModal">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Campaign</h5>
            <button type="button" class="btn-close" @click="closeEditModal">
              <CloseIcon class="close-icon" />
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleEditSubmit">
              <div class="mb-3">
                <label for="editTitle" class="form-label">Campaign Title</label>
                <input type="text" v-model="editTitle" class="form-control" id="editTitle" />
              </div>
              <div class="mb-3">
                <label for="editDescription" class="form-label">Campaign Description</label>
                <textarea v-model="editDescription" class="form-control" id="editDescription" rows="3"></textarea>
              </div>
              <div class="mb-3">
                <label for="editBudget" class="form-label">Campaign Budget</label>
                <input type="number" v-model="editBudget" class="form-control" id="editBudget" min="0"/>
              </div>
              <div class="d-flex justify-content-between">
                <div class="mb-3">
                  <label for="editStartDate" class="form-label">Start Date</label>
                  <input type="date" v-model="editStartDate" class="form-control" id="editStartDate" />
                  <div v-if="startDateError" class="text-danger">{{ startDateError }}</div>
                </div>
                <div class="mb-3">
                  <label for="editEndDate" class="form-label">End Date</label>
                  <input type="date" v-model="editEndDate" class="form-control" id="editEndDate" />
                  <div v-if="endDateError" class="text-danger">{{ endDateError }}</div>
                </div>
              </div>
              <div class="mb-3 form-check form-switch">
                <label class="form-check-label" for="editVisibility">Set as public</label>
                <input class="form-check-input" type="checkbox" v-model="editVisibility" id="editVisibility" />
              </div>

              <div v-if="!visibility" class="mb-3">
            <label for="influencer" class="form-label">Select Influencer</label>
            <select
              v-model="selectedInfluencer"
              class="form-control"
              id="influencer"
            >
              <option disabled value=""  class="form-control">Select an Influencer</option>
              <option v-for="influencer in influencers" :key="influencer.id" :value="influencer.id" class="form-control">
                {{ influencer.name }}
              </option>
            </select>
          </div>

              <div class="mb-3">
                <label for="editGoal" class="form-label">Campaign Goal</label>
                <input type="text" v-model="editGoal" class="form-control" id="editGoal" />
              </div>
              <button type="submit" class="btn btn-primary" :disabled="startDateError || endDateError">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { PencilSharp, TrashOutline, CloseOutline, GlobeOutline, LockClosedOutline } from '@vicons/ionicons5'
import axios from 'axios'
import { useUserStore } from '@/stores/user';

// Convert timestamp to YYYY-MM-DD format
const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toISOString().split('T')[0]
}

// Convert YYYY-MM-DD format to timestamp
const parseDate = (dateString) => {
  if (!dateString) return null
  return new Date(dateString).toISOString()
}

const props = defineProps({
  campaign: Object
})

const open = ref(false)
const startDateError = ref(null)
const endDateError = ref(null)
const editTitle = ref(props.campaign.campaign_name)
const editDescription = ref(props.campaign.campaign_desc)
const editBudget = ref(props.campaign.campaign_budget)
const editStartDate = ref(formatDate(props.campaign.campaign_start))
const editEndDate = ref(formatDate(props.campaign.campaign_end))
const editVisibility = ref(props.campaign.campaign_visibility === 'public')
const editGoal = ref(props.campaign.campaign_goal)
const influencers = ref([])
const emit = defineEmits(['campaign-fetch'])

const openEditModal = () => {
  open.value = true
}

const closeEditModal = () => {
  open.value = false
}
/*
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
    fetchInfluencers()
  }
})
*/
const validateDates = () => {
  if (editStartDate.value && editEndDate.value) {
    if (new Date(editStartDate.value) > new Date(editEndDate.value)) {
      startDateError.value = 'Start date cannot be after end date'
      endDateError.value = 'End date cannot be before start date'
    } else {
      startDateError.value = null
      endDateError.value = null
    }
  }
}

watch([editStartDate, editEndDate], validateDates)

const handleEditSubmit = async () => {
  if (startDateError.value || endDateError.value) {
    // Prevent form submission if there's an error
    return
  }
  
  try {
    await updateCampaign()
    closeEditModal()
    await fetchMyActiveCampaigns()
  } catch (error) {
    handleError(error)
  }
}

const deleteCampaign = async () => {
  const userStore = useUserStore();
  
  // Ensure the token is available from the user store
  const token = userStore.token;
    if (!token) {
      throw new Error('Authorization token is missing');
    }

    // Send the HTTP DELETE request
    await axios.delete(`http://localhost:5000/campaigns/${props.campaign.id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    emit('campaign-fetch');
    console.log('Campaign delete successfully');
}

const updateCampaign = async () => {
  const userStore = useUserStore();
  
  try {
    // Prepare the payload
    const payload = {
      name: editTitle.value,
      description: editDescription.value,
      budget: editBudget.value,
      start_date: editStartDate.value,
      end_date: editEndDate.value,
      visibility: editVisibility.value ? 'public' : 'private',
      goal: editGoal.value
    };

    // Ensure the token is available from the user store
    const token = userStore.token;
    if (!token) {
      throw new Error('Authorization token is missing');
    }

    // Send the HTTP PUT request
    await axios.put(`http://localhost:5000/campaigns/${props.campaign.id}`, payload, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    emit('campaign-fetch');
    console.log('Campaign updated successfully');
  } catch (error) {
    console.error('Failed to update campaign:', error);
    // Optionally, show an error message to the user
  }
};


const handleError = (error) => {
  console.error('Failed to update campaign:', error)
  // Optionally, show an error message to the user
}

const fetchMyActiveCampaigns = async () => {
  // Implement fetching active campaigns logic here
}

// Watch for changes in the props and update local state
watch(() => props.campaign, (newVal) => {
  editTitle.value = newVal.campaign_name
  editDescription.value = newVal.campaign_desc
  editBudget.value = newVal.campaign_budget
  editStartDate.value = formatDate(newVal.campaign_start)
  editEndDate.value = formatDate(newVal.campaign_end)
  editVisibility.value = newVal.campaign_visibility === 'public'
  editGoal.value = newVal.campaign_goal
}, { deep: true })
</script>

<style scoped>
/*.card .campaign-card {
  z-index: 1000;
  position: relative;
}*/

.card-header {
  background-color: #f7f7f7;
  padding: 1rem;
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-body {
  padding: 1rem;
  overflow: hidden;
}

.card-footer {
  background-color: #f7f7f7;
  padding: 1rem;
  border-top: 1px solid #ddd;
}

.edit-icon {
  width: 20px;
  height: auto;
}

.delete-icon {
  width: 20px;
  height: auto;
}

.close-icon {
  width: 20px;
  height: auto;
}

.visibility-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.public-icon,
.private-icon {
  width: 24px;
  height: 24px;
}

.modal-overlay {
  z-index: 10000;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-in;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 60rem;
  max-height: 80vh;
  z-index: 100;
  overflow-y: auto;
  padding: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease-in-out;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ddd;
}

.modal-body {
  padding: 1rem 0;
}

.modal-footer {
  padding: 1rem 0;
  border-top: 1px solid #ddd;
}

.visibility-label {
  text-transform: uppercase;
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.visibility-label {
  font-weight: bold;
  margin-top: 0.5rem;
}

.card-title,
.card-text {
  text-align: left;
}

.card-title strong,
.card-text strong {
  display: block;
}

/* .main-box {
  z-index: 1000;
  position: relative;
} */
</style>
