<template>
  <div class="header-wrapper">
    <!-- 删除这个重复的导航节点组件 -->
    <!-- <NavigationNodes class="navigation-nodes-component" /> -->
    
    <el-header class="custom-header">
      <div class="header-container">
        <el-row :gutter="3" class="main-row">
          <!-- First Column: Title and Navigation Nodes -->
          <el-col :span="19" class="content-container">
            <!-- Title Section -->
            <div class="title-container">
              <h2 class="dashboard-title">
                <span style="color: #86a779">Smart GBX Dashboard </span>
                <span style="color: #44652a">for HKUST(GZ) </span>
                <span style="color: #76c850">2025</span>
              </h2>
              <hr style="border-top: 2px solid #cbebc4; width: 90%; margin: 5px 0 0 5px" />
            </div>

            <!-- 替换原来的Statistic Cards Layout为Navigation Nodes -->
            <div class="navigation-container">
              <NavigationNodes />
            </div>
          </el-col>

          <!-- Second Column: SVG Image -->
          <el-col :span="5" class="svg-container">
            <img
              src="@/assets/Header.svg"
              alt="Descriptive Text"
              class="header-image"
            />
          </el-col>
        </el-row>
      </div>
    </el-header>
  </div>
</template>

<script setup>
import NavigationNodes from './NavigationNodes.vue';
</script>

<style scoped>
.header-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.navigation-nodes-component {
  margin-bottom: 10px;
}

.custom-header {
  background-color: #e3f0d878;
  color: #2f6d36;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 6px 10px;
  border-radius: 20px;
  height: auto;
  min-height: 160px;
}

.header-container {
  width: 100%;
  height: 100%;
}

.main-row {
  width: 100%;
  height: 100%;
}

.content-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.title-container {
  margin-bottom: 5px;
  margin-top: 0;
}

.dashboard-title {
  font-size: 2.2em;
  margin: 0;
  line-height: 1.1;
  text-align: left;
  width: 100%;
  font-weight: bold;
}

.navigation-container {
  flex: 1;
  display: flex;
  align-items: center;
  width: 100%;
  overflow: visible;
  margin-top: 10px;
  min-height: 90px;
}

.svg-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding-right: 0;
}

.header-image {
  width: auto;
  height: 100%;
  max-height: 130px;
  object-fit: contain;
  margin: 0 auto;
}

/* 响应式设计 */
@media screen and (max-width: 1920px) {
  .dashboard-title {
    font-size: 2em;
  }
  
  .navigation-container {
    margin-top: 5px;
  }
  
  .custom-header {
    min-height: 140px;
    padding: 5px 8px;
  }
}

@media screen and (max-width: 1440px) {
  .dashboard-title {
    font-size: 1.8em;
  }
}

@media screen and (max-width: 1280px) {
  .dashboard-title {
    font-size: 1.6em;
  }
}

/* 针对1680*3200屏幕的特定调整 */
@media screen and (width: 1680px) and (height: 3200px) {
  .custom-header {
    padding: 6px;
  }
  
  .dashboard-title {
    font-size: 2.2em;
  }
  
  .header-image {
    max-height: 100px;
  }

}

/* 添加深度选择器来覆盖 Element Plus 的默认样式 */
:deep(.el-icon) {
  vertical-align: middle !important;
}
</style>
