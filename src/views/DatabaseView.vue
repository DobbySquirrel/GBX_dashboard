<template>
  <div class="database-view">
    <h1>数据库内容浏览</h1>
    
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchTables">重试</button>
    </div>
    
    <div v-else class="database-content">
      <div class="tables-list">
        <h2>数据表列表</h2>
        <ul>
          <li 
            v-for="table in tables" 
            :key="table" 
            :class="{ active: selectedTable === table }"
            @click="selectTable(table)"
          >
            {{ table }}
          </li>
        </ul>
      </div>
      
      <div class="table-data" v-if="selectedTable">
        <h2>{{ selectedTable }} 表数据</h2>
        
        <div v-if="tableLoading" class="loading">
          <div class="spinner"></div>
          <p>加载表数据中...</p>
        </div>
        
        <div v-else-if="tableError" class="error">
          <p>{{ tableError }}</p>
          <button @click="fetchTableData(selectedTable)">重试</button>
        </div>
        
        <div v-else-if="tableData && tableData.data && tableData.data.length > 0" class="data-table">
          <div class="table-controls" v-if="!tableData.isEmpty">
            <div class="pagination">
              <button 
                :disabled="currentPage === 1" 
                @click="changePage(currentPage - 1)"
              >
                上一页
              </button>
              <span>{{ currentPage }} / {{ tableData.pagination.pages }}</span>
              <button 
                :disabled="currentPage === tableData.pagination.pages" 
                @click="changePage(currentPage + 1)"
              >
                下一页
              </button>
            </div>
            <div class="page-size">
              每页显示:
              <select v-model="pageSize" @change="changePageSize">
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
          </div>
          
          <div class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th v-for="column in tableColumns" :key="column">{{ column }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="tableData.isEmpty">
                  <td :colspan="tableColumns.length" class="empty-message">表中没有数据</td>
                </tr>
                <tr v-else v-for="(row, index) in tableData.data" :key="index">
                  <td v-for="column in tableColumns" :key="column">{{ row[column] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-else class="empty-data">
          <p>表中没有数据</p>
        </div>
      </div>
      
      <div class="table-placeholder" v-else>
        <p>请从左侧选择一个表查看数据</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { getAllTables, getTableData, getTableStructure } from '@/api/database';

export default {
  setup() {
    const loading = ref(false);
    const error = ref(null);
    const tables = ref([]);
    const selectedTable = ref(null);
    const tableData = ref(null);
    const tableLoading = ref(false);
    const tableError = ref(null);
    const currentPage = ref(1);
    const pageSize = ref(20);
    
    const tableColumns = computed(() => {
      if (!tableData.value || !tableData.value.data || tableData.value.data.length === 0) {
        return [];
      }
      return Object.keys(tableData.value.data[0]);
    });
    const fetchTables = async () => {
  loading.value = true;
  error.value = null;

  try {
    const tablesData = await getAllTables();
    console.log('获取到的表列表:', tablesData);

    // 过滤掉 null 值
    let filteredTables = tablesData.filter(table => table !== null);

    if (filteredTables.length === 0) {
      // 如果过滤后没有表，可能需要检查原始数据
      if (tablesData.length > 0 && typeof tablesData[0] === 'object') {
        // 尝试从对象中提取表名
        filteredTables = tablesData.map(item => {
          // 查找可能的表名属性
          const tableNameKey = Object.keys(item).find(key =>
            key.toLowerCase().includes('table') ||
            key.toLowerCase().includes('name')
          );
          return tableNameKey ? item[tableNameKey] : null;
        }).filter(name => name !== null);
      }
    }

    // 倒序排列表名

    tables.value = filteredTables.reverse();

  } catch (err) {
    console.error('获取表列表错误详情:', err);
    error.value = '获取表列表失败: ' + (err.message || '未知错误');
  } 
  finally {
    loading.value = false;
  }
};

const fetchTableData = async (tableName, page = 1, limit = pageSize.value) => {
  if (!tableName) return;

  tableLoading.value = true;
  tableError.value = null;

  try {
    const offset = (page - 1) * limit;
    const encodedTableName = encodeURIComponent(tableName);
    const response = await getTableData(encodedTableName, { limit, offset });

    // 如果表中没有数据，获取表结构以显示列名
    if (!response.data || response.data.length === 0) {
      try {
        const structure = await getTableStructure(encodedTableName);
        if (structure && structure.length > 0) {
          const columnKey = Object.keys(structure[0]).find(key =>
            key.toLowerCase().includes('column_name') ||
            key.toLowerCase().includes('field')
          );

          if (columnKey) {
            const emptyRow = {};
            structure.forEach(col => {
              emptyRow[col[columnKey]] = null;
            });

            tableData.value = {
              ...response,
              data: [emptyRow],
              isEmpty: true
            };
          }
        }
      } catch (structErr) {
        console.error('获取表结构错误:', structErr);
      }
    } else {
      // 对获取到的表数据进行倒序处理
      response.data.reverse();
      tableData.value = response;
    }

    currentPage.value = page;
  } catch (err) {
    console.error('获取表数据错误:', err);
    tableError.value = `获取表 ${tableName} 数据失败: ${err.message || '未知错误'}`;
  } finally {
    tableLoading.value = false;
  }
};    

    const selectTable = (tableName) => {
      selectedTable.value = tableName;
      currentPage.value = 1;
      fetchTableData(tableName);
    };
    
    const changePage = (page) => {
      fetchTableData(selectedTable.value, page);
    };
    
    const changePageSize = () => {
      currentPage.value = 1;
      fetchTableData(selectedTable.value, 1, pageSize.value);
    };
    
    onMounted(() => {
      fetchTables();
    });
    
    return {
      loading,
      error,
      tables,
      selectedTable,
      tableData,
      tableLoading,
      tableError,
      tableColumns,
      currentPage,
      pageSize,
      fetchTables,
      selectTable,
      changePage,
      changePageSize,
      fetchTableData
    };
  }
}
</script>

<style scoped>
.database-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.database-content {
  display: flex;
  gap: 20px;
}

.tables-list {
  flex: 0 0 250px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  background-color: #f9f9f9;
}

.tables-list h2 {
  margin-top: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.tables-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tables-list li {
  padding: 8px 10px;
  margin: 5px 0;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.tables-list li:hover {
  background-color: #eee;
}

.tables-list li.active {
  background-color: #1890ff;
  color: white;
}

.table-data, .table-placeholder {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
}

.table-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  color: #999;
  font-size: 16px;
}

.table-data h2 {
  margin-top: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination button {
  padding: 5px 10px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

tr:hover {
  background-color: #f9f9f9;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #1890ff;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  color: #f5222d;
  text-align: center;
  padding: 20px;
}

.error button {
  margin-top: 10px;
  padding: 5px 15px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.empty-data {
  text-align: center;
  padding: 30px;
  color: #999;
}

.empty-message {
  text-align: center;
  padding: 20px;
  color: #999;
  font-style: italic;
}
</style> 