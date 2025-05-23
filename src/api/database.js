// 数据库 API 接口
const API_BASE_URL = '/api';  // 使用相对路径，让代理处理

/**
 * 获取所有数据表
 * @returns {Promise<Array>} 表名列表
 */
export async function getAllTables() {
  try {
    const response = await fetch(`${API_BASE_URL}/tables`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || '获取表列表失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('获取表列表错误:', error);
    throw error;
  }
}

/**
 * 获取表结构
 * @param {string} tableName 表名
 * @returns {Promise<Array>} 表结构信息
 */
export async function getTableStructure(tableName) {
  try {
    const response = await fetch(`${API_BASE_URL}/tables/${tableName}/structure`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `获取表 ${tableName} 结构失败`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`获取表 ${tableName} 结构错误:`, error);
    throw error;
  }
}

/**
 * 获取表数据
 * @param {string} tableName 表名
 * @param {Object} options 分页选项
 * @param {number} options.limit 每页记录数
 * @param {number} options.offset 偏移量
 * @returns {Promise<Object>} 表数据和分页信息
 */
export async function getTableData(tableName, options = { limit: 20, offset: 0 }) {
  try {
    // 修复URL构造问题
    const baseUrl = `${API_BASE_URL}/tables/${tableName}`;
    const queryParams = new URLSearchParams();
    queryParams.append('limit', options.limit);
    queryParams.append('offset', options.offset);
    
    const url = `${baseUrl}?${queryParams.toString()}`;
    console.log('请求URL:', url); // 添加调试日志
    
    const response = await fetch(url);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `获取表 ${tableName} 数据失败`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`获取表 ${tableName} 数据错误:`, error);
    throw error;
  }
} 