import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import Echarts from 'vue-echarts';
import BaiduMapGL from 'vue3-baidu-map-gl';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

const app = createApp(App);

// 注册基础组件
app.use(ElementPlus);
app.use(createPinia());
app.use(router);
app.component('Echarts', Echarts);

// 注册图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 等待地图加载完成后注册百度地图
window.addEventListener('load', () => {
  app.use(BaiduMapGL, {
    ak: import.meta.env.VITE_BAIDU_MAP_AK
  });
  
  app.mount('#app');
});
