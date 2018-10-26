var MiniCssExtractPlugin = require('mini-css-extract-plugin')
var CopyWebpackPlugin = require('copy-webpack-plugin')
var webpack = require('webpack')
var path = require('path')
var autoprefixer = require('autoprefixer')

module.exports = {
  entry: {
    adhocracy4: [
      './meinberlin/assets/scss/style.scss',
      './meinberlin/assets/js/app.js'
    ],
    vendor: [
      'classnames',
      '@fortawesome/fontawesome-free-webfonts/scss/fontawesome.scss',
      '@fortawesome/fontawesome-free-webfonts/scss/fa-brands.scss',
      '@fortawesome/fontawesome-free-webfonts/scss/fa-regular.scss',
      '@fortawesome/fontawesome-free-webfonts/scss/fa-solid.scss',
      'jquery',
      'js-cookie',
      'react',
      'immutability-helper',
      'react-dom',
      'react-flip-move',
      'shariff/dist/shariff.complete.js',
      'shariff/dist/shariff.min.css'
    ],
    select2: [
      'select2'
    ],
    leaflet: [
      'leaflet',
      'mapbox-gl-leaflet',
      'mapbox-gl/dist/mapbox-gl.js',
      'leaflet/dist/leaflet.css',
      'leaflet.markercluster',
      'leaflet.markercluster/dist/MarkerCluster.css',
      './meinberlin/apps/plans/assets/plans_map.jsx'
    ],
    'mapboxgl': [
      'mapbox-gl/dist/mapbox-gl.js'
    ],
    datepicker: [
      './meinberlin/assets/js/init-picker.js',
      'datepicker/css/datepicker.min.css'
    ],
    embed: [
      './meinberlin/assets/js/embed.js'
    ],
    'popup-close': [
      './meinberlin/assets/js/popup-close.js'
    ],
    'map_choose_polygon_with_preset': [
      './meinberlin/apps/maps/assets/map_choose_polygon_with_preset.js',
      'leaflet-draw',
      'leaflet-draw/dist/leaflet.draw.css',
      './meinberlin/assets/js/i18n-leaflet-draw.js',
      'file-saver',
      'shpjs'
    ]
  },
  output: {
    libraryTarget: 'this',
    library: '[name]',
    path: path.resolve('./meinberlin/static/'),
    publicPath: '/static/',
    filename: '[name].js'
  },
  externals: {
    'django': 'django'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules\/(?!adhocracy4|bootstrap)/, // exclude most dependencies
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'].map(require.resolve)
        }
      },
      {
        test: /\.s?css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader
          },
          {
            loader: 'css-loader'
          },
          {
            loader: 'postcss-loader',
            options: {
              ident: 'postcss',
              plugins: (loader) => [
                autoprefixer()
              ]
            }
          },
          {
            loader: 'sass-loader'
          }
        ]
      },
      {
        test: /fonts\/.*\.(svg|woff2?|ttf|eot)(\?.*)?$/,
        loader: 'file-loader',
        options: {
          name: 'fonts/[name].[ext]'
        }
      },
      {
        test: /\.svg$|\.png$/,
        loader: 'file-loader',
        options: {
          name: 'images/[name].[ext]'
        }
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', '.scss', '.css'],
    alias: {
      'jquery$': 'jquery/dist/jquery.min.js',
      'shariff$': 'shariff/dist/shariff.complete.js'
    },
    // when using `npm link`, dependencies are resolved against the linked
    // folder by default. This may result in dependencies being included twice.
    // Setting `resolve.root` forces webpack to resolve all dependencies
    // against the local directory.
    modules: [path.resolve('./node_modules')]
  },
  plugins: [
    new webpack.ProvidePlugin({
      timeago: 'timeago.js'
    }),
    new webpack.optimize.SplitChunksPlugin({
      name: 'vendor',
      filename: 'vendor.js'
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css'
    }),
    new CopyWebpackPlugin([
      {
        from: './meinberlin/assets/images/**/*',
        to: 'images/',
        flatten: true
      },
      {
        from: './meinberlin/assets/info',
        to: 'info/',
        flatten: false
      }
    ])
  ]
}
