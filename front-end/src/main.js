import { createApp } from 'vue'
import App from './App.vue'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import * as Icons from '@element-plus/icons-vue'
import store from './store';


const app = createApp(App)

for (const [key, component] of Object.entries(Icons)) {
    app.component(key, component)
  }

app.use(ElementPlus)
app.use(router)
app.use(store)
app.mount('#app')

console.log('Element Plus has been installed!')
