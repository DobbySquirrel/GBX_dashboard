import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/GBX_Box_Web/',
  server: {
    proxy: {
      "/mapv": {
        target: "https://mapv.baidu.com",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/mapv/, ""),
      },
    },
  },
  plugins: [
    vue(),
    {
      name: 'html-transform',
      transformIndexHtml(html) {
        return html.replace(/%VITE_BAIDU_MAP_AK%/g, process.env.VITE_BAIDU_MAP_AK)
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    sourcemap: false,
    minify: 'terser',
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks: {
          'echarts': ['echarts'],
          'element-plus': ['element-plus']
        }
      }
    }
  }
})
