import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/homepage.vue'
import PageOne from '../views/pageone.vue'
import PageTwo from '../views/pagetwo.vue'
import PageThree from '../views/pagethree.vue'
import PageFour from '../views/pagefour.vue'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    component: HomePage,
    children: [
      {
        path: 'pageone',
        name: 'PageOne',
        component: PageOne
      },
      {
        path: 'pagetwo',
        name: 'PageTwo',
        component: PageTwo
      },
      {
        path: 'pagethree',
        name: 'PageThree',
        component: PageThree
      },
      {
        path: 'pagefour',
        name: 'PageFour',
        component: PageFour
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
