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
              <span style="color: #76c850">2024</span>
            </h2>
            <hr style="border-top: 2px solid #cbebc4; width: 90%; margin: 5px 0 0 5px" />
          </div>

          <!-- Statistic Cards Layout -->
          <el-row :gutter="5" class="statistic-row">
            <el-col :span="1" class="statistic-col"> </el-col>
            <el-col :span="6" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="energyCost"
                  value-style="font-size: 1.7em; color: #44652a;font-weight: bold;"
                >
                  <template #title>
                    <div
                      style="
                        display: inline-flex;
                        align-items: center;
                        font-size: 2em;
                        color: #44652a;
                      "
                    >
                    Carbon Reduction
                    </div>
                  </template>
                  <template #prefix>
                    <el-icon
                      style="vertical-align: -0.35em"
                      color="#76c850"
                      size="80"
                    >
                      <Odometer />
                    </el-icon>
                    <span style="margin-left: 10px"></span>
                  </template>
                  <template #suffix>
                    <el-text class="mx-1" style="font-size: 1em; color: #86a779"
                      ><span style="margin-left: 10px"></span>g CO2</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
            
            <el-col :span="6" class="statistic-col">
              <div style="font-size: 1em; color: #44652a;">
                = {{ energyCost / 0.5267 }} boxes * 0.5267g per box
              </div>
              <div style="font-size: 0.8em; color: #44652a; margin-top: 5px;">
                Notes: <br>1. Assumed 20 cycles for green boxes <br>2. Carbon reduction is compared with corrugated boxes of the same size and transport distance.
              </div>
            </el-col>

            <el-col :span="5" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="mealBoxRecycling"
                  value-style="font-size: 1.7em; color: #44652a;font-weight: bold;"
                >
                  <template #title>
                    <div
                      style="
                        display: inline-flex;
                        align-items: center;
                        font-size: 2em;
                        color: #44652a;
                      "
                    >
                      Box Recycling
                    </div>
                  </template>
                  <template #prefix>
                    <el-icon
                      style="vertical-align: -0.35em"
                      color="#76c850"
                      size="80"
                    >
                      <MessageBox />
                    </el-icon>
                    <span style="margin-left: 10px"></span>
                  </template>
                  <template #suffix>
                    <el-text class="mx-1" style="font-size: 1em; color: #86a779"
                      ><span style="margin-left: 10px"></span>Boxes</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
            <el-col :span="5" class="statistic-col">
              <div style="font-size: 1em; color: #44652a; ">
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
    
    // 统计 product_id 为 66dd1bb4eff8e33e5f3f233f 的数据行数
    const count = dataRows.filter(line => {
      const values = line.split(",");
      const product_id = values[1]?.trim();
      return product_id === '66dd1bb4eff8e33e5f3f233f';
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

    // 统计 Status 为 RecycleDelivery 的数据行数
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
  padding: 10px;
  border-radius: 30px;
  height: auto;
  min-height: 210px;
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
  margin-top: 10px;
}

.statistic-card {
  height: auto;
  padding: 10px;
}

.svg-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
  padding-right: 20px;
}

.header-image {
  max-width: 100%;
  max-height: 200px;
  width: auto;
  height: 200px;
  object-fit: contain;
  margin-right: 0;
}

.dashboard-title {
  font-size: 2em;
  margin: 0;
  line-height: 1.2;
  text-align: left;
  width: 100%;
}

.title-container {
  margin-bottom: 15px;
  margin-top: 0;
}
</style>
