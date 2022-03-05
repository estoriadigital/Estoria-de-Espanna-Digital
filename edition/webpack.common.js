const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: {
    main: path.resolve(__dirname, "src/assets/main.js")
  },
  module: {
    rules: [
      {
        test: /\.(woff|woff2|ttf)$/i,
        type: 'asset/resource'
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: path.resolve(__dirname, 'src/home.html'),
    }),
    new CopyPlugin({
      patterns: [
        {context: path.resolve(__dirname, "src/assets"),
          from: "data",
         to: path.resolve(__dirname, "dist/data")}
      ]
    })
  ],
};
