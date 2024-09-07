<template>
  <div class="table-responsive">
    <table class="table table-hover table-bordered">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Campaign Title</th>
          <th scope="col">Budget</th>
          <th scope="col">Visibility</th>
          <th scope="col">Start Date</th>
          <th scope="col">End Date</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody v-drag-and-drop>
        <tr v-for="(campaign, index) in campaigns" :key="campaign.id" @dragstart="dragStart(index)" @dragover.prevent @drop="drop(index)" draggable="true">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ campaign.campaign_name }}</td>
          <td>INR {{ campaign.campaign_budget }}</td>
          <td>
            <span v-if="campaign.campaign_visibility === 'public'" class="badge bg-success">Public</span>
            <span v-else class="badge bg-warning">Private</span>
          </td>
          <td>{{ formatDate(campaign.campaign_start) }}</td>
          <td>{{ formatDate(campaign.campaign_end) }}</td>
          <td>
            <button @click="openEditModal(campaign)" class="btn btn-primary btn-sm m-1">
              <PencilSharp class="edit-icon" />
            </button>
            <button @click="deleteCampaign(campaign.id)" class="btn btn-danger btn-sm m-1">
              <TrashOutline class="delete-icon" />
            </button>
            <button @click="viewCampaign(campaign.id)" class="btn btn-info btn-sm m-1">
              View
            </button>
          </td>
        </tr>
      </tbody>
    </table>

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
            <p><strong>Goal:</strong> {{ viewCampaignData.campaign_goal }}</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { PencilSharp, TrashOutline, CloseIcon } from '@vicons/ionicons5'
import { useUserStore } from '@/stores/user'

// Campaigns data (replace this with your data fetching logic)
const campaigns = ref([])

const viewOpen = ref(false)
const viewCampaignData = ref({})
const dragging = ref(null)

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toISOString().split('T')[0]
}

const viewCampaign = async (id) => {
  const userStore = useUserStore()
  const token = userStore.token
  try {
    const response = await axios.get(`http://localhost:5000/campaigns/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    viewCampaignData.value = response.data
    viewOpen.value = true
  } catch (error) {
    console.error('Failed to fetch campaign:', error)
  }
}

const closeViewModal = () => {
  viewOpen.value = false
}

const dragStart = (index) => {
  dragging.value = index
}

const drop = (index) => {
  const draggedCampaign = campaigns.value[dragging.value]
  campaigns.value.splice(dragging.value, 1)
  campaigns.value.splice(index, 0, draggedCampaign)
  dragging.value = null
}

const openEditModal = (campaign) => {
  // Open edit modal (Implement modal logic here)
}

const deleteCampaign = async (id) => {
  const userStore = useUserStore()
  const token = userStore.token
  try {
    await axios.delete(`http://localhost:5000/campaigns/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    // Fetch updated campaigns after delete (implement fetch logic)
  } catch (error) {
    console.error('Failed to delete campaign:', error)
  }
}
</script>

<style scoped>
.table-responsive {
  margin: 1rem 0;
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

tr[draggable="true"] {
  cursor: move;
}
</style>
