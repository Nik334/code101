<template>
  <div>
    <div class="card text-center campaign-card">
      <div class="card-body">
        <h5 class="card-title">
          {{ ad.messages }}
        </h5>
        <p class="card-text">
          {{ ad.requirements }}
        </p>
        <div>
          <!-- <button
            @click="() => fetchCampaign(props.id)"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
            class="btn btn-primary"
          >
            View
          </button> -->
          <button @click="() => acceptRequest(ad.id)" class="btn btn-primary mx-2">Accept</button>
          <button class="btn btn-primary" @click="() => rejectRequest(ad.id)">Reject</button>
        </div>
      </div>
      <div class="card-footer text-muted">INR {{ ad.payment_amount }}</div>
    </div>
    <!-- Modal -->
    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">View Campaign</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="card text-center campaign-card">
              <div class="card-header">{{ campaignById.campaign_visibility }}</div>
              <div class="card-body">
                <h5 class="card-title">
                  {{ campaignById.campaign_name }} - INR {{ campaignById.campaign_budget }}
                </h5>
                <p class="card-text">
                  {{ campaignById.campaign_desc }}
                </p>
              </div>
              <div class="card-footer text-muted">
                {{ campaignById.campaign_start }} - {{ campaignById.campaign_end }}
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const props = defineProps(['ad'])
const emit = defineEmits(['request-accepted', 'refresh-requests'])

const campaignById = ref([])

const fetchCampaign = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/campaigns/${props.ad.id}`)
    console.log(response.data)
    campaignById.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const acceptRequest = async (id) => {
  try {
    await axios
      .put(
        `http://localhost:5000/ads/${id}/accept`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      )
      .then((response) => {
        console.log(response.data)
        emit('request-accepted')
        emit('refresh-requests')
      })
      .catch((error) => {
        console.error(error)
      })
  } catch (error) {
    console.error(error)
  }
}

const rejectRequest = async (id) => {
  try {
    await axios
      .put(
        `http://localhost:5000/ads/${id}/reject`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      )
      .then((response) => {
        console.log(response.data)
        emit('refresh-requests')
      })
      .catch((error) => {
        console.error(error)
      })
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
.campaign-card {
  width: 300px;
}
</style>
