const webpack = require('webpack')
const path = require('path')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
  entry: {
    adhocracy4: [
      '@fortawesome/fontawesome-free/scss/fontawesome.scss',
      '@fortawesome/fontawesome-free/scss/brands.scss',
      '@fortawesome/fontawesome-free/scss/regular.scss',
      '@fortawesome/fontawesome-free/scss/solid.scss',
      'shariff/dist/shariff.min.css',
      'select2/dist/css/select2.min.css',
      'slick-carousel/slick/slick.css',
      './meinberlin/assets/extra_css/_slick-theme.css',
      './meinberlin/assets/scss/style.scss',
      './meinberlin/assets/js/app.js'
    ],
    captcheck: {
      import: [
        './meinberlin/apps/captcha/assets/captcheck.js'
      ],
      dependOn: 'adhocracy4'
    },
    datepicker: {
      import: [
        './meinberlin/assets/js/init-picker.js',
        'datepicker/css/datepicker.min.css'
      ],
      dependOn: 'adhocracy4'
    },
    embed: {
      import: [
        'bootstrap/js/dist/modal.js',
        './meinberlin/apps/embed/assets/embed.js'
      ],
      dependOn: 'adhocracy4'
    },
    dsgvo_video_embed: {
      import: [
        'dsgvo-video-embed/dist/dsgvo-video-embed.min.css',
        'dsgvo-video-embed/dist/dsgvo-video-embed.min.js'
      ],
      dependOn: 'adhocracy4'
    },
    blueprint_picker: {
      import: [
        './meinberlin/assets/js/blueprint-picker.js'
      ],
      dependOn: 'adhocracy4'
    },
    // these do not rely on adhocracy and adding the depend causes console error
    // error possibly due to needing to be loaded at specific time
    documents: {
      import: './meinberlin/apps/documents/assets/react_documents_init.js'
    },
    budget_proposals: {
      import: './meinberlin/apps/budgeting/assets/react_proposals_init.js'
    },
    unload_warning: {
      import: './meinberlin/assets/js/unload_warning.js'
    },
    // A4 dependencies - we want all of them to go through webpack
    mb_plans_map: {
      import: [
        'leaflet/dist/leaflet.css',
        'mapbox-gl/dist/mapbox-gl.css',
        'leaflet.markercluster/dist/MarkerCluster.css',
        'react-bootstrap-typeahead/css/Typeahead.css',
        './meinberlin/apps/plans/assets/plans_map.jsx'
      ],
      dependOn: 'adhocracy4'
    },
    a4maps_display_point: {
      import: [
        'leaflet/dist/leaflet.css',
        'mapbox-gl/dist/mapbox-gl.css',
        'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_display_point.js'
      ],
      dependOn: 'adhocracy4'
    },
    a4maps_display_points: {
      import: [
        'leaflet/dist/leaflet.css',
        'mapbox-gl/dist/mapbox-gl.css',
        'leaflet.markercluster/dist/MarkerCluster.css',
        'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_display_points.js'
      ],
      dependOn: 'adhocracy4'
    },
    a4maps_choose_point: {
      import: [
        'leaflet/dist/leaflet.css',
        'mapbox-gl/dist/mapbox-gl.css',
        'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_choose_point.js'
      ],
      dependOn: 'adhocracy4'
    },
    a4maps_choose_polygon: {
      import: [
        'leaflet/dist/leaflet.css',
        'mapbox-gl/dist/mapbox-gl.css',
        'leaflet-draw/dist/leaflet.draw.css',
        './meinberlin/apps/maps/assets/map_choose_polygon_with_preset.js'
      ],
      dependOn: 'adhocracy4'
    },
    category_formset: {
      import: [
        'adhocracy4/adhocracy4/categories/assets/category_formset.js'
      ],
      dependOn: 'adhocracy4'
    },
    image_uploader: {
      import: [
        'adhocracy4/adhocracy4/images/assets/image_uploader.js'
      ],
      dependOn: 'adhocracy4'
    },
    select_dropdown_init: {
      import: [
        'adhocracy4/adhocracy4/categories/assets/select_dropdown_init.js'
      ],
      dependOn: 'adhocracy4'
    },
    budgeting_disable_contact: {
      import: [
        './meinberlin/apps/budgeting/assets/disable_contact.js'
      ]
    }
  },
  output: {
    libraryTarget: 'this',
    library: '[name]',
    path: path.resolve('./meinberlin/static/'),
    publicPath: '/static/'
  },
  externals: {
    django: 'django'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules\/(?!(adhocracy4)\/).*/, // exclude most dependencies
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'].map(require.resolve),
          plugins: ['@babel/plugin-transform-runtime', '@babel/plugin-transform-modules-commonjs']
        }
      },
      {
        test: /\.s?css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader
          },
          {
            loader: 'css-loader',
            options: {
              url: {
                filter: (url, resourcePath) => {
                  // only handle `/` urls, leave rest in code (pythong images to be left)
                  if (!url.startsWith('/')) {
                    return true
                  } else {
                    return false
                  }
                }
              }
            }
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  require('autoprefixer')
                ]
              }
            }
          },
          {
            loader: 'sass-loader'
          }
        ]
      },
      {
        test: /fonts\/.*\.(svg|woff2?|ttf|eot)(\?.*)?$/,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name][ext]'
        }
      },
      {
        test: /\.svg$|\.png$/,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name][ext]'
        }
      }
    ]
  },
  resolve: {
    fallback: { path: require.resolve('path-browserify') },
    extensions: ['*', '.js', '.jsx', '.scss', '.css'],
    alias: {
      bootstrap$: 'bootstrap/dist/js/bootstrap.bundle.min.js',
      jquery$: 'jquery/dist/jquery.min.js',
      select2$: 'select2/dist/js/select2.min.js',
      shariff$: 'shariff/dist/shariff.min.js',
      shpjs$: 'shpjs/dist/shp.min.js',
      tether$: 'tether/dist/js/tether.min.js',
      'slick-carousel$': 'slick-carousel/slick/slick.min.js'
    },
    // when using `npm link`, dependencies are resolved against the linked
    // folder by default. This may result in dependencies being included twice.
    // Setting `resolve.root` forces webpack to resolve all dependencies
    // against the local directory.
    modules: [path.resolve('./node_modules')]
  },
  plugins: [
    new webpack.ProvidePlugin({
      timeago: 'timeago.js',
      $: 'jquery',
      jQuery: 'jquery',
      Promise: ['es6-promise', 'Promise'],
      fetch: ['whatwg-fetch', 'fetch']
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[name].css'
    }),
    new CopyWebpackPlugin({
      patterns: [{
        from: './meinberlin/assets/images/**/*',
        to: 'images/[name][ext]'
      }]
    })
  ]
}
