const path = require("path");
const common = require("./webpack.common");
const merge = require("webpack-merge");
const { CleanWebpackPlugin }= require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require('webpack-bundle-tracker');

module.exports = merge(common, {
  mode: "development",
  output: {
    filename: "[name]-[contentHash].js",
    path: path.resolve(__dirname, "./assets/bundles/dev")
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: "[name]-[contentHash].css" }),
    new CleanWebpackPlugin(),
    new BundleTracker({path: __dirname, filename: './assets/bundles/dev/stats.json'})
  ],
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          "style-loader", //3. Inject styles into DOM
          "css-loader", //2. Turns css into commonjs
          "sass-loader" //1. Turns sass into css
        ]
      },
      {
        test: /\.css$/,
        use: [
          "style-loader",
          "css-loader"
        ]
      }
    ]
  },
  devServer: {
    hot: true,
    compress: true,
    publicPath: '/assets/bundles/dev/'
  },
});