import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import axios from 'axios'

// Request interceptor
axios.interceptors.request.use((config) => {
    // Modify the request config here
    return config
})

// Response interceptor
axios.interceptors.response.use((response) => {
    console.log("inside response interceptor");
    // Handle the response here
    return response
}, (error) => {
    if (error?.response?.status === 401) {
        router.push('/login');
    }

    // Handle errors here
    console.error(error)
    return Promise.reject(error)
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
