const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  mode: 'production',
  context: __dirname,
  entry: './assets/src/js/index.tsx',
  resolve: {
    extensions: ['.tsx','.ts','.js'],
//    alias: {
//         'react-native$': 'react-native-web',
//    },
  },
  output: {
    path: path.resolve('./assets/dist/'),
    filename: "[name].[contenthash].js"
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],
  module: {
    rules: [
      {
        test: /\.tsx?$/i,
        loader: 'ts-loader',
        exclude: /node_modules/,
//        include: [path.resolve('./assets/src/js/**/**/**'),path.resolve('./assets/src/js/index.tsx')]
      },
      {
        test: /\.js|\.jsx$/,
        include: path.resolve("./assets/dist/**"),
//        exclude: /node_modules/,
        loader: 'babel-loader',
      }
//      {
//        test: /\.js$/,
//        include: /node_modules\/react-native/,
//        use: {
//            loader: 'babel-loader',
//            options: {
//                cacheDirectory: true,
//                plugins: ['react-native-web'],
//                presets: ['module:metro-react-native-babel-preset'],
//            },
//       },
//      },
    ],
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
    }
  }
}

