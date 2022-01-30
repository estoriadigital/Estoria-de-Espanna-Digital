const path = require('path');
const common = require("./webpack.common");
const merge = require("webpack-merge").merge;
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = merge(common, {
  mode: "production",
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].bundle.js',
    clean: true
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader']
      },
      {
        test: /\.(woff|woff2|ttf|svg|eot)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[hash][ext][query]'
        }
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({filename: '[name].[contenthash].css'})
  ]
});
