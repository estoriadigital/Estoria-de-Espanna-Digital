const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: {
    main: path.resolve(__dirname, "src/main.js"),
    deps: path.resolve(__dirname, "src/deps.js")
  },
  module: {
    rules: [
      // {
      //   test: /\.(json)/,
      //   type: 'asset/resource'
      // }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: path.resolve(__dirname, 'src/home.html'),
    })
  ],
};
