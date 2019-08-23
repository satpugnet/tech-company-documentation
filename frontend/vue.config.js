const webpack = require('webpack');

module.exports = {
  runtimeCompiler: true,
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        $: 'jquery',
        jquery: 'jquery',
        jQuery: 'jquery',
        'window.jQuery': 'jquery'
      })
    ]
  },
  publicPath: '/',
  outputDir: 'dist',
  assetsDir: 'static',
  indexPath: 'index.html',
  filenameHashing: true,

  // Only used for the dev web_server
  devServer: {
    // This proxies all the calls to flask that start with a /api (makes it look like we only have 1 origin)
    proxy: {
      '/api/*': {
        target: 'http://localhost:5000',
        ws: true,
        changeOrigin: true,
        followRedirects: true
      }
    }
  }
};