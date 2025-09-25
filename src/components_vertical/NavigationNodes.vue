<template>
  <div class="navigation-nodes">
    <div class="nodes-container">
      <div 
        v-for="(node, index) in nodes" 
        :key="index" 
        class="node-item"
        :class="{ 'active': isActive(node.route) }"
        @click="navigateTo(node.route)"
      >
        <div class="node-circle">
          <el-icon v-if="node.icon" :size="20">
            <component :is="node.icon" />
          </el-icon>
        </div>
        <div class="node-label">{{ node.label }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Van, Box, School, Place } from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute();

const nodes = [
  { label: '无人车', icon: Van, route: '/vehicle' },
  { label: '外卖员', icon: Box, route: '/delivery' },
  { label: '无人机', icon: Place, route: '/drone' },
  { label: '环境', icon: School, route: '/environment' }
];

const isActive = (path) => {
  return route.path === path;
};

const navigateTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
.navigation-nodes {
  width: 100%;
  padding: 10px 0;
  background-color: #f5f9f200;
  border-radius: 15px;
  margin-bottom: 10px;
  min-height: 100px;
}

.nodes-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  padding: 0 40px;
  width: 100%;
  box-sizing: border-box;
  min-height: 80px;
}

.node-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
  flex: 1;
}

/* 重新设计连接线 */
.nodes-container::before {
  content: '';
  position: absolute;
  top: 30px;
  left: 70px;
  right: 70px;
  height: 2px;
  background-color: #86a779;
  z-index: 1;
}

.node-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #e3f0d8;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 2px solid #cbebc4;
  position: relative;
  z-index: 3;
}

.node-label {
  margin-top: 8px;
  font-size: 14px;
  font-weight: bold;
  color: #44652a;
  transition: all 0.3s ease;
}

/* 移除原来的连接线 */
.connector-line {
  display: none;
}

.node-item.active .node-circle {
  transform: scale(1.2);
  background-color: #76c850;
  border-color: #44652a;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.node-item.active .node-label {
  font-size: 16px;
  color: #2f6d36;
}

.node-item:hover .node-circle {
  transform: scale(1.1);
  background-color: #cbebc4;
}

/* 响应式设计 */
@media screen and (max-width: 1280px) {
  .node-circle {
    width: 50px;
    height: 50px;
  }
  
  .node-label {
    font-size: 12px;
  }
  
  .node-item.active .node-label {
    font-size: 14px;
  }
  
  .nodes-container::before {
    top: 25px;
  }
}

@media screen and (max-width: 768px) {
  .nodes-container {
    padding: 0 20px;
  }
  
  .node-circle {
    width: 40px;
    height: 40px;
  }
  
  .node-label {
    font-size: 10px;
  }
  
  .node-item.active .node-label {
    font-size: 12px;
  }
  
  .nodes-container::before {
    top: 20px;
    left: 40px;
    right: 40px;
  }
}

/* 添加更多响应式调整 */
@media screen and (max-height: 800px) {
  .navigation-nodes {
    min-height: 80px;
    padding: 5px 0;
  }
  
  .node-circle {
    width: 45px;
    height: 45px;
  }
  
  .node-label {
    margin-top: 5px;
    font-size: 12px;
  }
}

/* 针对特别宽的屏幕 */
@media screen and (min-width: 1920px) {
  .navigation-nodes {
    min-height: 120px;
  }
  
  .node-circle {
    width: 70px;
    height: 70px;
  }
  
  .nodes-container::before {
    top: 35px;
  }
}
</style> 