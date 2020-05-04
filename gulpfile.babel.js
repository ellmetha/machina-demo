import '@babel/polyfill';

import ExtractTextPlugin from 'extract-text-webpack-plugin';
import gulp from 'gulp';
import env from 'gulp-env';
import gutil from 'gulp-util';
import path from 'path';
import webpack from 'webpack';
import WebpackDevServer from 'webpack-dev-server';
import ManifestPlugin from 'webpack-manifest-plugin';

/* Global variables */
const rootDir = `${__dirname}/`;
const staticDir = `${rootDir}main/static/`;
const PROD_ENV = gutil.env.production;
const WEBPACK_DEV_SERVER_PORT = (
  process.env.WEBPACK_DEV_SERVER_PORT ? process.env.WEBPACK_DEV_SERVER_PORT : 8080);
env.set({ NODE_ENV: PROD_ENV ? 'production' : 'debug' });

/* Directories */
const buildDir = PROD_ENV ? `${staticDir}build` : `${staticDir}build_dev`;
const lessDir = `${staticDir}less`;
const jsDir = `${staticDir}js`;


/*
 * Global webpack config
 * ~~~~~~~~~~~~~~~~~~~~~
 */

const webpackConfig = {
  mode: PROD_ENV ? 'production' : 'development',
  entry: {
    App: [`${jsDir}/App.js`, `${lessDir}/App.less`],
  },
  output: {
    filename: 'js/[name].js',
    path: buildDir,
    publicPath: PROD_ENV ? '/static/build/' : '/static/build_dev/',
  },
  resolve: {
    modules: ['bower_components', 'node_modules', ],
    extensions: ['.webpack.js', '.web.js', '.js', '.jsx', '.json', 'less'],
  },
  module: {
    rules: [
      { test: /\.jsx?$/, exclude: /node_modules/, use: 'babel-loader' },
      { test: /\.less$/,
        use: ExtractTextPlugin.extract(
            { use: ['css-loader', 'less-loader'], fallback: 'style-loader', publicPath: '../' }) },
      { test: /\.txt$/, use: 'raw-loader' },
      { test: /\.(png|jpg|jpeg|gif|svg|woff|woff2)([\?]?.*)$/, use: 'url-loader?limit=10000' },
      { test: /\.(eot|ttf|wav|mp3|otf)([\?]?.*)$/, use: 'file-loader' },
    ],
  },
  optimization: {
    minimize: PROD_ENV,
  },
  plugins: [
    new ExtractTextPlugin({ filename: 'css/[name].css', disable: false }),
    ...(PROD_ENV ? [
      new webpack.LoaderOptionsPlugin({
        minimize: true,
      }),
    ] : []),
  ],
};


/*
 * Webpack task
 * ~~~~~~~~~~~~
 */

/* Task to build our JS and CSS applications. */
gulp.task('build-webpack-assets', gulp.series(() => (
  new Promise((resolve, reject) => {
    // eslint-disable-next-line consistent-return
    webpack(webpackConfig, (err, stats) => {
      if (err) {
        return reject(err);
      }
      if (stats.hasErrors()) {
        return reject(new Error(stats.compilation.errors.join('\n')));
      }
      console.log(stats.toString({
        chunks: false,
        colors: true,
      }));
      resolve();
    });
  })
)));


/*
 * Global tasks
 * ~~~~~~~~~~~~
 */

gulp.task('build', gulp.series('build-webpack-assets'));


/*
 * Development tasks
 * ~~~~~~~~~~~~~~~~~
 */

gulp.task('webpack-dev-server', () => {
  const devWebpackConfig = Object.create(webpackConfig);
  devWebpackConfig.devtool = 'eval';
  devWebpackConfig.devServer = { hot: true };
  devWebpackConfig.entry = {
    App: [
      `${jsDir}/App.js`, `${lessDir}/App.less`,
      `webpack-dev-server/client?http://localhost:${WEBPACK_DEV_SERVER_PORT}`,
      'webpack/hot/only-dev-server',
    ],
  };
  devWebpackConfig.module = {
    rules: [
      { test: /\.jsx?$/, exclude: /node_modules/, use: 'babel-loader' },
      { test: /\.less$/, use: ['style-loader', 'css-loader', 'less-loader'] },
      { test: /\.txt$/, use: 'raw-loader' },
      { test: /\.(png|jpg|jpeg|gif|svg|woff|woff2)([\?]?.*)$/, use: 'url-loader?limit=10000' },
      { test: /\.(eot|ttf|wav|mp3|otf)([\?]?.*)$/, use: 'file-loader' },
    ],
  };
  devWebpackConfig.output = {
    path: path.resolve(__dirname, staticDir),
    publicPath: `http://localhost:${WEBPACK_DEV_SERVER_PORT}/static/`,
    filename: 'js/[name].js',
  };
  devWebpackConfig.plugins = [
    new webpack.LoaderOptionsPlugin({ debug: true }),
    new webpack.HotModuleReplacementPlugin(),
  ];

  // Start a webpack-dev-server
  new WebpackDevServer(webpack(devWebpackConfig), {
    contentBase: path.resolve(__dirname, staticDir, '..'),
    publicPath: '/static/',
    hot: true,
    inline: true,
  }).listen(WEBPACK_DEV_SERVER_PORT, 'localhost', (err) => {
    if (err) throw new gutil.PluginError('webpack-dev-server', err);
    gutil.log(
      '[webpack-dev-server]',
      `http://localhost:${WEBPACK_DEV_SERVER_PORT}/webpack-dev-server/`);
  });
});
