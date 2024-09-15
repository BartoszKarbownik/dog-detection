import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './style.css';
import App from './App.vue';
import router from './router';
import VueTheMask from 'vue-the-mask';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faDog } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faDog);

const app = createApp(App);

app.component('font-awesome-icon', FontAwesomeIcon);


app.use(router);
app.use(createPinia()); 
app.use(VueTheMask);

app.mount('#app');
