// eslint-disable-next-line no-undef
const { defineConfig } = require('@vue/cli-service')
// eslint-disable-next-line no-undef
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        // eslint-disable-next-line no-undef
        target: process.env.DEBUG_BASE_URL,  // 设置后端接口的访问地址
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''  // 将请求路径中的 '/api' 替换为空字符串
        // }
      }
    }
  }
})
