const { defineConfig } = require('@vue/cli-service')

module.exports = {

  outputDir: '../myapp/static',

  indexPath: '../templates/index.html',

  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : '/',

  devServer: {

    proxy: 'http://localhost:8000',

  },

};