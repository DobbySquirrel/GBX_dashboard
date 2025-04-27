<template>
  <el-header class="custom-header">
    <div class="header-container">
      <el-row :gutter="3" class="main-row">
        <!-- First Column: Title and Statistic Cards -->
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

          <!-- Statistic Cards Layout -->
          <el-row :gutter="6" class="statistic-row">
            <el-col :span="5" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="energyCost"
                  value-style="font-size: 1em; color: #44652a; font-weight: bold;"
                >
                  <template #title>
                  </template>
                  <template #prefix>
                    <el-icon
                      class="statistic-icon"
                      color="#76c850"
                    >
                      <Odometer />
                    </el-icon>
                    <span style="margin-left: 5px"></span>
                  </template>
                  <template #suffix>
                    <el-text class="mx-1" style="font-size: 0.6em; color: #86a779"
                      ><span style="margin-left: 5px"></span>g CO2</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
            
            <el-col :span="8" class="statistic-col">
              <div style="font-size: 14px; color: #44652a; font-weight: bold;">
                = {{ Math.round(energyCost / 0.5267) }} boxes * 0.5267g per box
              </div>
              <div style="font-size: 14px; color: #44652a; margin-top: 5px; font-weight: bold;">
                Notes: <br>1. Assumed 20 cycles for green boxes <br>2. Carbon reduction is compared with corrugated boxes of the same size and transport distance
              </div>
            </el-col>

            <el-col :span="5" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="mealBoxRecycling"
                  value-style="font-size: 1em; color: #44652a; font-weight: bold;"
                >
                  <template #title>
                  </template>
                  <template #prefix>
                    <el-icon
                      class="statistic-icon"
                      color="#76c850"
                    >
                      <MessageBox />
                    </el-icon>
                    <span style="margin-left: 5px"></span>
                  </template>
                  <template #suffix>
                    <el-text class="mx-1" style="font-size: 0.6em; color: #86a779"
                      ><span style="margin-left: 5px"></span>Boxes</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
            <el-col :span="6" class="statistic-col">
              <div style="font-size: 16px; color: #44652a; font-weight: bold;">
                = Number of Recycling boxes placed in the locker
              </div>
            </el-col>
          </el-row>
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
</template>

<script setup>
import { defineProps, computed } from 'vue';
import {
  Odometer,
  Van,
  MessageBox,
} from "@element-plus/icons-vue";

const props = defineProps({
  DeliveryDrone_Property_DroneDeliveryOrder: {
    type: [String, null],
    required: true,
  },
  IndoorDeliveryCar_Property_IndoorDeliveryOrder: {
    type: [String, null],
    required: true,
  },
  OutdoorDeliveryCar_Property_OutdoorDeliveryOrder: {
    type: [String, null],
    required: true,
  },
  Delivery_Locker_Property_RecycleDelivery: {
    type: [String, null],
    required: true,
  },
  Box_owner: {
    type: [String, null],
    required: true,
  },
});

// 计算 Energy Cost
const energyCost = computed(() => {
  if (!props.Box_owner) return 0;
  
  try {
    const lines = props.Box_owner.trim().split("\n");
    const dataRows = lines.slice(1); // 跳过表头行
    
    // 计算 Status 为 'RecycleInDelivery' 的数量
    const count = dataRows.filter(line => {
      const values = line.split(",");
      const status = values[3]?.trim();
      return status === 'RecycleInDelivery';
    }).length;
    
    // 返回数量 * 0.5267
    return count * 0.5267;
  } catch (error) {
    console.error('Error calculating energy cost:', error);
    return 0;
  }
});

// 计算 Meal Box Recycling
const mealBoxRecycling = computed(() => {
  if (!props.Box_owner) return 0;

  try {
    const lines = props.Box_owner.trim().split("\n");
    const dataRows = lines.slice(1); // 跳过表头行
    
    // 计算 Status 为 'RecycleInDelivery' 的数量
    const count = dataRows.filter(line => {
      const values = line.split(",");
      const status = values[3]?.trim();
      return status === 'RecycleInDelivery';
    }).length;

    return count;
    
  } catch (error) {
    console.error('Error calculating meal box recycling:', error);
    return 0;
  }
});
</script>

<style scoped>
.custom-header {
  background-color: #E3F0D8;
  color: #2f6d36;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 6px;
  border-radius: 20px;
  height: 100%;
  min-height: 0;
  overflow: hidden;
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
  margin-bottom: 3px;
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

.statistic-row {
  width: 100%;
  height: auto;
  margin-top: 2px;
}

.statistic-card {
  height: auto;
  padding: 2px;
  white-space: nowrap;  /* 防止内容换行 */
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
  max-height: 150px;
  object-fit: contain;
  margin: 0 auto;
}

.statistic-icon {
  font-size: 1.4em;  /* 进一步减小图标大小 */
  vertical-align: middle;
}

/* 响应式设计 */
@media screen and (max-width: 1920px) {
  .dashboard-title {
    font-size: 2em;
  }
  
  .statistic-icon {
    font-size: 1.6em;  /* 减小图标大小 */
  }
}

@media screen and (max-width: 1440px) {
  .dashboard-title {
    font-size: 1.8em;
  }
  
  .statistic-icon {
    font-size: 1.4em;  /* 减小图标大小 */
  }
}

@media screen and (max-width: 1280px) {
  .dashboard-title {
    font-size: 1.6em;
  }
  
  .statistic-icon {
    font-size: 1.2em;  /* 减小图标大小 */
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
  
  .statistic-icon {
    font-size: 1.8em;  /* 减小图标大小 */
  }
  
  :deep(.el-statistic__title) {
    font-size: 1.6em !important;
    margin-bottom: 6px !important;
    font-weight: bold !important;
  }
  
  :deep(.el-statistic__content) {
    font-size: 1.6em !important;
    font-weight: bold !important;
    white-space: nowrap !important;  /* 防止内容换行 */
  }
  
  .header-image {
    max-height: 180px;
  }
}

/* 添加深度选择器来覆盖 Element Plus 的默认样式 */
:deep(.el-icon) {
  vertical-align: middle !important;
}

:deep(.el-statistic__title) {
  font-size: 1.6em;
  margin-bottom: 6px;
  font-weight: bold;
}

:deep(.el-statistic__content) {
  font-size: 1.6em;
  font-weight: bold;
  white-space: nowrap;  /* 防止内容换行 */
}

/* 增加说明文字的大小 */
.statistic-col div {
  font-size: 1.1em !important;
  line-height: 1.3;
}

/* 修复后缀文本换行问题 */
:deep(.el-statistic__content-suffix) {
  white-space: nowrap;
  display: inline-block;
  font-size: 0.5em !important;  /* 减小后缀文本大小 */
  margin-left: 5px !important;  /* 减小左边距 */
}

/* 确保数值和后缀之间有足够间距 */
:deep(.el-statistic__content-value) {
  margin-right: 3px;
}

/* 确保所有统计数值具有相同的样式 */
:deep(.el-statistic__content-value) {
  font-size: 1.4em !important;
  font-weight: bold !important;
  color: #44652a !important;
  margin-right: 3px;
}

/* 确保所有后缀具有相同的样式 */
:deep(.el-statistic__content-suffix) {
  white-space: nowrap;
  display: inline-block;
  font-size: 0.5em !important;
  margin-left: 5px !important;
  color: #86a779 !important;
}
</style>
