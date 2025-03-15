<template>
  <el-header class="custom-header">
    <div class="header-container">
      <el-row :gutter="3" class="main-row">
        <!-- First Column: Title and Statistic Cards -->
        <el-col :span="18" class="content-container">
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
          <el-row :gutter="5" class="statistic-row">
            <el-col :span="1" class="statistic-col"> </el-col>
            <el-col :span="5" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="energyCost"
                  value-style="font-size: 1.2em; color: #44652a;font-weight: bold;"
                >
                  <template #title>
                    <div
                      style="
                        display: inline-flex;
                        align-items: center;
                        font-size: 1.2em;
                        color: #44652a;
                      "
                    >
                    Carbon Reduction
                    </div>
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
                    <el-text class="mx-1" style="font-size: 0.8em; color: #86a779"
                      ><span style="margin-left: 10px"></span>g CO2</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
            
            <el-col :span="8" class="statistic-col">
              <div style="font-size: 0.5em; color: #44652a;">
                = {{ Math.round(energyCost / 0.5267) }} boxes * 0.5267g per box
              </div>
              <div style="font-size: 10px; color: #44652a; margin-top: 5px;">
                Notes: <br>1. Assumed 20 cycles for green boxes <br>2. Carbon reduction is compared with corrugated boxes of the same size and transport distance
              </div>
            </el-col>

            <el-col :span="4" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="mealBoxRecycling"
                  value-style="font-size: 1.2em; color: #44652a;font-weight: bold;"
                >
                  <template #title>
                    <div
                      style="
                        display: inline-flex;
                        align-items: center;
                        font-size: 1.2em;
                        color: #44652a;
                      "
                    >
                      Box Recycling
                    </div>
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
                    <el-text class="mx-1" style="font-size: 0.8em; color: #86a779"
                      ><span style="margin-left: 10px"></span>Boxes</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
            <el-col :span="5" class="statistic-col">
              <div style="font-size: 10px; color: #44652a; ">
                = Number of Recycling boxes placed in the locker
              </div>

            </el-col>
          </el-row>
        </el-col>

        <!-- Second Column: SVG Image -->
        <el-col :span="6" class="svg-container">
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
  padding: 8px;
  border-radius: 30px;
  height: auto;
  min-height: 170px;
}

.header-container {
  width: 100%;
  height: auto;
}

.main-row {
  width: 100%;
  height: auto;
}

.content-container {
  display: flex;
  flex-direction: column;
  height: auto;
}

.statistic-row {
  width: 100%;
  height: auto;
  margin-top: 5px;
}

.statistic-card {
  height: auto;
  padding: 5px;
}

.svg-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
  padding-right: 10px;
}

.header-image {
  width: auto;
  height: calc(100% - 20px);
  max-height: 130px;
  min-height: 120px;
  object-fit: contain;
  margin-right: 0;
}

.dashboard-title {
  font-size: 1.5em;
  margin: 0;
  line-height: 1.1;
  text-align: left;
  width: 100%;
}

.title-container {
  margin-bottom: 8px;
  margin-top: 0;
}

@media screen and (max-width: 1920px) {
  .header-image {
    max-height: 130px;
  }
}

@media screen and (max-width: 1440px) {
  .header-image {
    max-height: 110px;
  }
}

@media screen and (max-width: 1280px) {
  .header-image {
    max-height: 90px;
  }
}

.statistic-icon {
  font-size: 2.5em;
  vertical-align: middle;
}

/* 响应式设计 */
@media screen and (max-width: 1920px) {
  .statistic-icon {
    font-size: 2.2em;
  }
}

@media screen and (max-width: 1440px) {
  .statistic-icon {
    font-size: 2em;
  }
}

@media screen and (max-width: 1280px) {
  .statistic-icon {
    font-size: 1.8em;
  }
}

/* 添加深度选择器来覆盖 Element Plus 的默认样式 */
:deep(.el-icon) {
  vertical-align: middle !important;
}
</style>
