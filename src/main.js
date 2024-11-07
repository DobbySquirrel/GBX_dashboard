import { createApp } from 'vue';
import Echarts from 'vue-echarts';
import App from './App.vue';
import './styles/element/index.scss'
import 'element-plus/dist/index.css';
import ElementPlus from 'element-plus';
import BaiduMapGL from 'vue3-baidu-map-gl';

// 创建应用实例
const app = createApp(App);

// 注册组件，使用小写 Echarts
app.component('Echarts', Echarts);

// 使用 Element Plus
app.use(ElementPlus);
app.use(BaiduMapGL, {
    ak: 'Yp57V71dkOPiXjiN8VdcFRsVELzlVNKK'
  })

// 挂载到 #app
app.mount('#app');
