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
      <div v-if="!admin">
        <button @click="o" class="btn btn-primary m-2">
          <PencilSharp class="edit-icon" />
        </button>
        <button @click="deleteCampaign(campaign.id)" class="btn btn-danger">
          <TrashOutline class="delete-icon" />
        </button>
      </div>
      <div v-else>
        <button v-if="!flagged" @click="setFlag()" class="btn btn-danger m-2">
          Flag
        </button>
        <button v-else @click="setUnFlag()" class="btn btn-primary">
          Unflagged
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
                <input type="number" v-model="editBudget" class="form-control" id="editBudget" min="0" />
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

              <!-- Influencer Dropdown -->
              <div class="mb-3">
                <label for="editInfluencer" class="form-label">Select Influencer</label>
                <select v-model="editInfluencer" class="form-select" id="editInfluencer">
                  <option v-for="influencer in influencers" :key="influencer.id" :value="influencer.id">
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
import '../assets/campaign-card.css';

import { PencilSharp, TrashOutline, CloseOutline, GlobeOutline, LockClosedOutline } from '@vicons/ionicons5'
import axios from 'axios'
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia'

// Convert timestamp to YYYY-MM-DD format
const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toISOString().split('T')[0]
}

const props = defineProps({
  campaign: Object,
  influencers: Array,  // List of influencers passed as a prop
  admin: Boolean,
  flagged: Boolean
})

const open = ref(false)
const startDateError = ref(null)
const endDateError = ref(null)
const influencers = ref([])
const editTitle = ref(props.campaign.campaign_name)
const editDescription = ref(props.campaign.campaign_desc)
const editBudget = ref(props.campaign.campaign_budget)
const editStartDate = ref(formatDate(props.campaign.campaign_start))
const editEndDate = ref(formatDate(props.campaign.campaign_end))
const editVisibility = ref(props.campaign.campaign_visibility === 'public')
const editInfluencer = ref(props.campaign.influencer_id) // Prepopulate with current influencer ID
const editGoal = ref(props.campaign.campaign_goal)
const emit = defineEmits(['campaign-fetch'])
const handleError = ref(null) // This should be a ref holding error messages

// Access the user store
const userStore = useUserStore()
const { token } = storeToRefs(userStore)

const openEditModal = () => {
  open.value = true
}

const closeEditModal = () => {
  open.value = false
}

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
    return
  }
  
  console.log("Campaign before changes:", props.campaign)
  
  try {
    await updateCampaign()
    closeEditModal()
    await fetchMyActiveCampaigns()
  } catch (error) {
    handleError.value = 'Failed to update campaign: ' + error.message // Set error message here
  }
}

const updateCampaign = async () => {
  
  try {
    // Prepare the payload including influencer ID
    const payload = {
      name: editTitle.value,
      description: editDescription.value,
      budget: editBudget.value,
      start_date: editStartDate.value,
      end_date: editEndDate.value,
      visibility: editVisibility.value ? 'public' : 'private',
      influencer_id: editInfluencer.value, // Now passing influencer_id
      goal: editGoal.value
    };

    console.log("Campaign after changes:", payload)

    if (!token) {
      throw new Error('Authorization token is missing');
    }

    await axios.put(`http://localhost:5000/campaigns/${props.campaign.id}`, payload, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    });

    emit('request-campaign');
    console.log('Campaign updated successfully');
  } catch (error) {
    console.error('Failed to update campaign:', error);
    handleError.value = 'Failed to update campaign: ' + error.message // Set error message here
  }
};

const setFlag = async () => {
  // console.log("userStore.token", token);
  try {
    const response = await axios.put(`http://localhost:5000/flag-campaign/${props.campaign.id}`, {}, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    });
    emit('request-campaign');
  } catch (error) {
    console.error('Failed to fetch influencers:', error);
    handleError.value = 'Failed to fetch influencers: ' + error.message // Set error message here
  }
}

const setUnFlag = async () => {
  // console.log("userStore.token", token);
  try {
    const response = await axios.put(`http://localhost:5000/unflag-campaign/${props.campaign.id}`, {}, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    });
    emit('request-campaign');
  } catch (error) {
    console.error('Failed to fetch influencers:', error);
    handleError.value = 'Failed to fetch influencers: ' + error.message // Set error message here
  }
}

onMounted(() => {
  fetchInfluencers(); // Fetch influencers on mount
})

const fetchInfluencers = async () => {
  const userStore = useUserStore();
  const token = userStore.token;
  try {
    const response = await axios.get('http://localhost:5000/influencers', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    influencers.value = response.data;
  } catch (error) {
    console.error('Failed to fetch influencers:', error);
    handleError.value = 'Failed to fetch influencers: ' + error.message // Set error message here
  }
};

watch(() => props.campaign, (newVal) => {
  editTitle.value = newVal.campaign_name
  editDescription.value = newVal.campaign_desc
  editBudget.value = newVal.campaign_budget
  editStartDate.value = formatDate(newVal.campaign_start)
  editEndDate.value = formatDate(newVal.campaign_end)
  editVisibility.value = newVal.campaign_visibility === 'public'
  editInfluencer.value = newVal.influencer_id // Ensure it updates the influencer ID, not name
  editGoal.value = newVal.campaign_goal
}, { deep: true })
</script>
