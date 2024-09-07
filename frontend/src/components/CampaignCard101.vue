<template>
  <div class="table-responsive">
    <table class="table table-bordered table-striped table-hover">
      <thead class="thead-dark">
        <tr>
          <th>Visibility</th>
          <th>Campaign Title</th>
          <th>Budget</th>
          <th>Description</th>
          <th>Start Date</th>
          <th>End Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <div class="visibility-icon">
              <PublicIcon v-if="campaign.campaign_visibility === 'public'" />
              <PrivateIcon v-else />
            </div>
            {{ campaign.campaign_visibility }}
          </td>
          <td>{{ campaign.campaign_name }}</td>
          <td>INR {{ campaign.campaign_budget }}</td>
          <td>{{ campaign.campaign_desc }}</td>
          <td>{{ formatDate(campaign.campaign_start) }}</td>
          <td>{{ formatDate(campaign.campaign_end) }}</td>
          <td>
            <button @click="openEditModal" class="btn btn-primary m-2">
              <PencilSharp class="edit-icon" />
            </button>
            <button @click="deleteCampaign(campaign.id)" class="btn btn-danger m-2">
              <TrashOutline class="delete-icon" />
            </button>
            <button @click="viewCampaign(campaign.id)" class="btn btn-info m-2">
              View
            </button>
          </td>
        </tr>
      </tbody>
    </table>

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

    <!-- View Modal for displaying campaign details -->
    <transition name="fade">
      <div v-if="viewOpen" class="modal-overlay" @click.self="closeViewModal">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Campaign Details</h5>
            <button type="button" class="btn-close" @click="closeViewModal">
              <CloseIcon class="close-icon" />
            </button>
          </div>
          <div class="modal-body">
            <p><strong>Campaign Name:</strong> {{ viewCampaignData.campaign_name }}</p>
            <p><strong>Budget:</strong> INR {{ viewCampaignData.campaign_budget }}</p>
            <p><strong>Description:</strong> {{ viewCampaignData.campaign_desc }}</p>
            <p><strong>Start Date:</strong> {{ formatDate(viewCampaignData.campaign_start) }}</p>
            <p><strong>End Date:</strong> {{ formatDate(viewCampaignData.campaign_end) }}</p>
            <p><strong>Influencer:</strong> {{ viewCampaignData.influencer?.name || 'N/A' }}</p>
            <p><strong>Goal:</strong> {{ viewCampaignData.campaign_goal }}</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { PencilSharp, TrashOutline, CloseIcon, PublicIcon, PrivateIcon } from '@vicons/ionicons5'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

// Convert timestamp to YYYY-MM-DD format
const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toISOString().split('T')[0]
}

const props = defineProps({
  campaign: Object,
  influencers: Array // List of influencers passed as a prop
})

const open = ref(false)
const viewOpen = ref(false)
const editTitle = ref(props.campaign.campaign_name)
const editDescription = ref(props.campaign.campaign_desc)
const editBudget = ref(props.campaign.campaign_budget)
const editStartDate = ref(formatDate(props.campaign.campaign_start))
const editEndDate = ref(formatDate(props.campaign.campaign_end))
const editVisibility = ref(props.campaign.campaign_visibility === 'public')
const editInfluencer = ref(props.campaign.influencer_id)
const editGoal = ref(props.campaign.campaign_goal)
const viewCampaignData = ref({})
const startDateError = ref(null)
const endDateError = ref(null)

const openEditModal = () => { open.value = true }
const closeEditModal = () => { open.value = false }
const closeViewModal = () => { viewOpen.value = false }

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
  if (startDateError.value || endDateError.value) return
  await updateCampaign()
  closeEditModal()
  emit('campaign-fetch')
}

const updateCampaign = async () => {
  const userStore = useUserStore()
  const token = userStore.token
  const payload = {
    name: editTitle.value,
    description: editDescription.value,
    budget: editBudget.value,
    start_date: editStartDate.value,
    end_date: editEndDate.value,
    visibility: editVisibility.value ? 'public' : 'private',
    influencer_id: editInfluencer.value,
    goal: editGoal.value
  }
  await axios.put(`http://localhost:5000/campaigns/${props.campaign.id}`, payload, {
    headers: { Authorization: `Bearer ${token}` }
  })
}

const viewCampaign = async (id) => {
  const userStore = useUserStore()
  const token = userStore.token
  const response = await axios.get(`http://localhost:5000/campaigns/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  viewCampaignData.value = response.data
  viewOpen.value = true
}

const deleteCampaign = async (id) => {
  const userStore = useUserStore()
  const token = userStore.token
  await axios.delete(`http://localhost:5000/campaigns/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  emit('campaign-fetch')
}
</script>

<style scoped>
/* Styles for responsiveness and appearance */
.table-responsive {
  margin: 1rem 0;
}

.visibility-icon {
  display: inline-block;
  margin-right: 5px;
}

thead th {
  background-color: #2d3e50; /* Adjust based on your theme */
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
}

.edit-icon {
  color: white;
}

.delete-icon {
  color: white;
}

.close-icon {
  color: black;
}
</style>
