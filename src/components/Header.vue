<template>
  <el-header class="custom-header" height="105%">
    <div class="header-container">
      <el-row :gutter="18" class="main-row">
        <!-- First Column: Title and Statistic Cards -->
        <el-col :span="18" class="content-container">
          <!-- Title Section -->
          <div class="title-container" style="text-align: left">
            <h2 style="font-size: 2.5em">
              <span style="color: #86a779">Smart GBX Dashboard </span>
              <span style="color: #44652a">for HKUST(GZ) </span>
              <span style="color: #76c850">2024</span>
            </h2>
            <hr style="border-top: 2px solid #cbebc4; width: 65%; margin: -10px 0 0 0" />
          </div>

          <!-- Statistic Cards Layout -->
          <el-row :gutter="15" class="statistic-row">
            <el-col :span="1" class="statistic-col"> </el-col>
            <el-col :span="7" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="9502"
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
                      Energy Cost
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
                      ><span style="margin-left: 10px"></span>CO2</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
            <el-col :span="7" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="15"
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
                      Meal Box Recycling
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
            <el-col :span="7" class="statistic-col">
              <div class="statistic-card">
                <el-statistic
                  :value="10"
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
                      Number of Orders
                    </div>
                  </template>
                  <template #prefix>
                    <el-icon
                      style="vertical-align: -0.35em"
                      color="#76c850"
                      size="80"
                    >
                      <Van />
                    </el-icon>
                    <span style="margin-left: 10px"></span>
                  </template>
                  <template #suffix>
                    <el-text class="mx-1" style="font-size: 1em; color: #86a779"
                      ><span style="margin-left: 10px"></span>Orders</el-text
                    >
                  </template>
                </el-statistic>
              </div>
            </el-col>
          </el-row>
        </el-col>

        <!-- Second Column: SVG Image -->
        <el-col :span="6" class="svg-container">

          <img
            src="@/assets/Header.svg"
            alt="Descriptive Text"
            style="width: 75% ;margin: 20px 0 0 0"
          />
        </el-col>
      </el-row>
    </div>
  </el-header>
</template>

<script lang="ts" setup>
import {
  ArrowRight,
  CaretBottom,
  Odometer,
  Van,
  MessageBox,
  CaretTop,
  Warning,
} from "@element-plus/icons-vue";
</script>

<style scoped>
.custom-header {
  background-color: #E3F0D8;

  color: #2f6d36;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
}

.title-container {
  margin-bottom: 5px;
  margin-top: -5px;
}

.statistic-row {
  margin-top: 15px;
  margin-bottom: 5px;
}

.svg-container {
  display: flex;
  justify-content: center;
  align-items: right;
  height: 90%;
}

</style>
