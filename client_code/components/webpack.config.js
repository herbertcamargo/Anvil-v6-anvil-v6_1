const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
  entry: {
    'react': './src/react/index.js',
    'vue': './src/vue/index.js',
    'service-worker-registration': './src/service-worker-registration.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, '../../theme/js'),
    library: '[name]Components',
    libraryTarget: 'umd',
    globalObject: 'this'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin()
  ],
  resolve: {
    extensions: ['.js', '.jsx', '.vue']
  },
  externals: {
    'react': 'React',
    'react-dom': 'ReactDOM',
    'vue': 'Vue'
  },
  performance: {
    hints: false
  }
}; 