import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/Signup.vue'),
    },
    {
      path: '/sponsor-dashboard',
      name: 'sponsor-dashboard',
      component: () => import('../views/SponsorDashboard.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: 'profile',
          name: 'sponsor-profile',
          component: () => import('../views/SponsorProfile.vue'),
        },
        {
          path: 'campaigns',
          name: 'sponsor-campaigns',
          component: () => import('../views/SponsorCampaign.vue'),
        }
      ],
    },
    {
      path: '/update',
      name: 'profile-update',
      component: () => import('../views/ProfileIndex.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/influencer-dashboard',
      name: 'influencer-dashboard',
      component: () => import('../views/InfluencerDashboard.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: 'profile',
          name: 'influencer-profile',
          component: () => import('../views/InfluencerDashboardProfile.vue'),
        },
        {
          path: 'campaigns',
          name: 'influencer-campaigns',
          component: () => import('../views/InfluencerDashboardCampaign.vue'),
        }
      ],
    },
    {
      path: '/admin-dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true },
    },
  ]
})

export default router;
