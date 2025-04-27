<template>
  <div class="order-panel">
    <div class="panel-header">
      <h2>订单显示面板</h2>
    </div>
    
    <div class="orders-container">
      <TransitionGroup name="order-list">
        <div v-for="order in filteredOrders" :key="order.id" class="order-card">
          <div class="order-content">
            <div class="order-icon">
              <img :src="getOrderIcon(order.type)" alt="订单图标">
            </div>
            <div class="order-details">
              <div class="order-id">订单号: {{ order.id }}</div>
              <div class="order-item">商品名称: {{ order.itemName }}</div>
              <div class="order-customer">客户: {{ order.customer }}</div>
              <div class="order-delivery">配送方式: {{ order.deliveryMethod }}</div>
              <div class="order-status" :class="getStatusClass(order.status)">
                订单状态: {{ order.status }}
              </div>
            </div>
          </div>
        </div>
        <div v-if="filteredOrders.length === 0" :key="'no-results'" class="no-results">
          没有找到匹配的订单
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderDisplayPanel',
  props: {
    orders: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      orderIcons: {
        package: '/box-icon.svg',
        food: '/food-icon.svg',
        default: '/default-icon.svg'
      },
      generatedOrders: [],
      orderInterval: null,
      orderTypes: ['package', 'food', 'express', 'document', 'default'],
      deliveryMethods: ['快递', '自提', '同城配送', '专车配送', '无人机配送', '无人车配送'],
      statuses: ['准备中', '配送中', '已送达', '已取消', '失败', '待取件'],
      foodItems: ['汉堡套餐', '披萨', '炒面', '牛排', '沙拉', '寿司', '炸鸡', '火锅', '奶茶', '咖啡', '蛋糕', '冰淇淋'],
      packageItems: ['电子产品', '服装', '图书', '家居用品', '化妆品', '玩具', '办公用品', '手机', '电脑', '耳机', '相机', '手表']
    };
  },
  computed: {
    filteredOrders() {
      // 如果有传入的订单则显示传入的，否则显示生成的
      return this.orders.length > 0 ? [...this.orders] : this.generatedOrders;
    }
  },
  mounted() {
    // 初始生成5个随机订单
    this.generateRandomOrders(5);
    
    // 每1秒添加一个新订单
    this.orderInterval = setInterval(() => {
      this.addRandomOrder();
    }, 1000);
  },
  beforeUnmount() {
    // 组件销毁前清除定时器
    if (this.orderInterval) {
      clearInterval(this.orderInterval);
    }
  },
  methods: {
    getOrderIcon(type) {
      return this.orderIcons[type] || this.orderIcons.default;
    },
    
    generateRandomOrders(count) {
      const newOrders = [];
      for (let i = 0; i < count; i++) {
        newOrders.push(this.createRandomOrder());
      }
      this.generatedOrders = newOrders;
    },
    
    addRandomOrder() {
      // 添加一个新订单到顶部
      this.generatedOrders.unshift(this.createRandomOrder());
      
      // 如果订单超过10个，删除最旧的
      if (this.generatedOrders.length > 10) {
        this.generatedOrders.pop();
      }
    },
    
    createRandomOrder() {
      const type = this.orderTypes[Math.floor(Math.random() * this.orderTypes.length)];
      const items = type === 'food' ? this.foodItems : this.packageItems;
      
      return {
        id: 'ORD' + Math.floor(Math.random() * 1000000).toString().padStart(6, '0'),
        type: type,
        itemName: items[Math.floor(Math.random() * items.length)],
        customer: '客户' + Math.floor(Math.random() * 1000),
        deliveryMethod: this.deliveryMethods[Math.floor(Math.random() * this.deliveryMethods.length)],
        status: this.statuses[Math.floor(Math.random() * this.statuses.length)],
        timestamp: new Date().getTime()
      };
    },
    
    getStatusClass(status) {
      switch(status) {
        case '准备中':
          return 'status-preparing';
        case '配送中':
          return 'status-delivering';
        case '已送达':
          return 'status-delivered';
        case '已取消':
          return 'status-cancelled';
        case '失败':
          return 'status-failed';
        case '待取件':
          return 'status-pending';
        default:
          return '';
      }
    }
  }
};
</script>

<style scoped>
.order-panel {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(221, 221, 221, 0.4);
  border-radius: 8px;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.8);
  box-sizing: border-box;
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding-top: 5px;
}

.panel-header {
  padding: 8px 15px;
  flex-shrink: 0;
  background-color: rgba(245, 245, 245, 0.5);
  border-bottom: 1px solid rgba(221, 221, 221, 0.4);
}

.panel-header h2 {
  margin: 0;
  font-size: 16px;
  text-align: center;
  color: #333;
  font-weight: 600;
}

.orders-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 15px 10px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  width: 100%;
  max-height: calc(100% - 45px);
}

.orders-container::-webkit-scrollbar {
  width: 4px;
}

.orders-container::-webkit-scrollbar-track {
  background: rgba(241, 241, 241, 0.5);
  border-radius: 2px;
}

.orders-container::-webkit-scrollbar-thumb {
  background: rgba(190, 190, 190, 0.5);
  border-radius: 2px;
}

.orders-container::-webkit-scrollbar-thumb:hover {
  background: rgba(170, 170, 170, 0.7);
}

.order-card {
  width: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  padding: 6px 8px;
  margin-bottom: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  box-sizing: border-box;
  transition: all 0.3s ease;
  border: none;
  overflow: hidden;
  flex-shrink: 0;
  min-height: 60px;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.order-card:first-child {
  background-color: rgba(240, 240, 240, 0.8);
  border-left: 3px solid #1890ff;
  animation: highlight-new-order 2s ease-in-out;
}

.order-content {
  display: flex;
  width: 100%;
  box-sizing: border-box;
}

.order-icon {
  width: 28px;
  height: 28px;
  margin-right: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(245, 245, 245, 0.7);
  border-radius: 6px;
}

.order-icon img {
  width: 18px;
  height: 18px;
}

.order-details {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  padding-right: 5px;
}

.order-id, .order-item, .order-customer, .order-delivery, .order-status {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.order-id {
  font-weight: bold;
  color: #666666;
  margin-bottom: 2px;
  font-size: 12px;
}

.order-item, .order-customer, .order-delivery {
  margin-bottom: 2px;
  font-size: 11px;
  color: #333;
}

.order-status {
  display: inline-block;
  margin-top: 2px;
  padding: 0px 5px;
  border-radius: 8px;
  font-size: 10px;
  background-color: rgba(245, 245, 245, 0.7);
}

.status-preparing {
  background-color: rgba(250, 173, 20, 0.2) !important;
  color: #d48806 !important;
}

.status-delivering {
  background-color: rgba(150, 150, 150, 0.2) !important;
  color: #666666 !important;
}

.status-delivered {
  background-color: rgba(82, 196, 26, 0.2) !important;
  color: #389e0d !important;
}

.status-cancelled {
  background-color: rgba(190, 190, 190, 0.2) !important;
  color: #888888 !important;
}

.status-failed {
  background-color: rgba(245, 34, 45, 0.2) !important;
  color: #cf1322 !important;
}

.status-pending {
  background-color: rgba(24, 144, 255, 0.2) !important;
  color: #1890ff !important;
}

.no-results {
  text-align: center;
  padding: 30px 0;
  color: #999;
  font-size: 14px;
}

/* 添加过渡动画样式 */
.order-list-enter-active,
.order-list-leave-active {
  transition: all 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28);
}

.order-list-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.9);
}

.order-list-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.order-list-move {
  transition: transform 0.8s ease;
}

/* 针对1680*3200屏幕的特定调整 */
@media screen and (width: 1680px) and (height: 3200px) {
  .panel-header h2 {
    font-size: 24px;
  }
  
  .order-id {
    font-size: 18px;
  }
  
  .order-item, .order-customer, .order-delivery {
    font-size: 16px;
  }
  
  .order-status {
    font-size: 14px;
    padding: 3px 10px;
  }
  
  .order-icon {
    width: 50px;
    height: 50px;
  }
  
  .order-icon img {
    width: 30px;
    height: 30px;
  }
}

@keyframes highlight-new-order {
  0% {
    background-color: rgba(24, 144, 255, 0.2);
  }
  100% {
    background-color: rgba(240, 240, 240, 0.8);
  }
}
</style> 