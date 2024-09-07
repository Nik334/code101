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
        <!-- Show the 'Accept' button if the status is 'Requested' -->
        <button 
          v-if="campaign.campaign_status === 'Pending'"
          class="btn btn-success me-2" 
          @click="updateCampaignStatus(campaign.id, 'Accepted')"
        >
          Accept
        </button>
        <!-- Show the 'Reject' button if the status is 'Requested' -->
        <button 
          v-if="campaign.campaign_status === 'Pending'"
          class="btn btn-danger"
          @click="updateCampaignStatus(campaign.id, 'Rejected')"
        >
          Reject
        </button>
        <!-- Always show the 'View' button -->
        <button @click="viewCampaign(campaign.id)" class="btn btn-info">
          View
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
      <!-- Display status message -->
      <p class="card-text">Status: {{ campaign.campaign_status }}</p>
    </main>
    <footer class="card-footer">
      <div>
        <strong>Start Date:</strong> {{ formatDate(campaign.campaign_start) }}
        <strong>End Date:</strong> {{ formatDate(campaign.campaign_end) }}
      </div>
    </footer>

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
            <p><strong>Status:</strong> {{ viewCampaignData.campaign_status }}</p> <!-- Display status here -->
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import '../assets/campaign-card.css';

const props = defineProps({
  campaign: Object,
});

const emit = defineEmits(['status-updated']); // Add this line to define the event

const viewOpen = ref(false);
const viewCampaignData = ref({});
const statusMessage = ref('');

const formatDate = (timestamp) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toISOString().split('T')[0];
}

const openViewModal = () => {
  viewOpen.value = true;
};

const closeViewModal = () => {
  viewOpen.value = false;
};

const viewCampaign = async (id) => {
  const userStore = useUserStore();
  const token = userStore.token;
  try {
    const response = await axios.get(`http://localhost:5000/campaigns/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    viewCampaignData.value = response.data;
    viewOpen.value = true;
  } catch (error) {
    console.error('Failed to fetch campaign:', error);
  }
};

const updateCampaignStatus = async (campaignId, status) => {
  try {
    await axios.put(`http://localhost:5000/campaigns/${campaignId}/status`, 
      { status }, 
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
    statusMessage.value = `Campaign status updated to ${status} successfully.`;
     emit('campaign-fetch');
    setTimeout(() => statusMessage.value = '', 3000); // Clear message after 3 seconds
  } catch (error) {
    console.error('Error updating campaign status:', error.response ? error.response.data : error.message);
    statusMessage.value = 'Failed to update status.';
    setTimeout(() => statusMessage.value = '', 3000); // Clear message after 3 seconds
  }
};
</script>

<style scoped>
.status-message {
  color: green; /* Green color for success messages */
  font-weight: bold;
  margin-top: 10px;
}
</style>
