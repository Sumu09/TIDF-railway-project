////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
import { src, dest, parallel, series, task, watch } from 'gulp';
import pjson from './package.json' with {type: 'json'};

// Plugins
import autoprefixer from 'autoprefixer';
import browserSyncLib from 'browser-sync';
import concat from 'gulp-concat';
import tildeImporter from 'node-sass-tilde-importer';
import cssnano from 'cssnano';
import pixrem from 'pixrem';
import plumber from 'gulp-plumber';
import postcss from 'gulp-postcss';
import rename from 'gulp-rename';
import rtlcss from "gulp-rtlcss";
import gulpSass from 'gulp-sass';
import * as dartSass from 'sass';
import gulUglifyES from 'gulp-uglify-es';
import npmdist from "gulp-npm-dist";

const browserSync = browserSyncLib.create();
const reload = browserSync.reload;
const sass = gulpSass(dartSass);
const uglify = gulUglifyES.default;

// Relative paths function
function pathsConfig() {
  const appName = `./${pjson.name}`;
  const vendorsRoot = 'node_modules';

  return {
    vendorsJs: [
      `${vendorsRoot}/@popperjs/core/dist/umd/popper.js`,
      `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`,
      `${vendorsRoot}/jquery/dist/jquery.min.js`,
      `${vendorsRoot}/lucide/dist/umd/lucide.min.js`,
      `${vendorsRoot}/simplebar/dist/simplebar.min.js`,
      `${vendorsRoot}/iconify-icon/dist/iconify-icon.min.js`,
      `${vendorsRoot}/flatpickr/dist/flatpickr.min.js`,
      `${vendorsRoot}/select2/dist/js/select2.min.js`,
      `${vendorsRoot}/inputmask/dist/inputmask.min.js`,
      `${vendorsRoot}/choices.js/public/assets/scripts/choices.min.js`,
      `${vendorsRoot}/nouislider/dist/nouislider.min.js`
    ],
    app: appName,
    templates: `${appName}/templates`,
    css: `${appName}/static/css`,
    sass: `${appName}/static/scss`,
    fonts: `${appName}/static/fonts`,
    images: `${appName}/static/images`,
    js: `${appName}/static/js`,
  };
}

const paths = pathsConfig();

////////////////////////////////
// Tasks
////////////////////////////////

const processCss = [
  autoprefixer(), // adds vendor prefixes
  pixrem(), // add fallbacks for rem units
];

const minifyCss = [
  cssnano({ preset: 'default' }), // minify result
];

// Styles autoprefixing and minification
function styles() {

  src([`${paths.sass}/app.scss`, `${paths.sass}/icons.scss`])
    .pipe(
      sass({
        importer: tildeImporter,
        includePaths: [paths.sass],
      }).on('error', sass.logError),
    )
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css))

  return src([`${paths.sass}/**/*.scss`])
    .pipe(
      sass({
        importer: tildeImporter,
        includePaths: [paths.sass],
      }).on('error', sass.logError),
    )
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rtlcss())
    .pipe(rename({ suffix: "-rtl.min", }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css));
}

// Javascript minification
function scripts() {
  return src(`${paths.js}/app.js`)
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js));
}

// Vendor Javascript minification
function vendorScripts() {
  return src(paths.vendorsJs, { sourcemaps: true })
    .pipe(concat('vendors.js'))
    .pipe(dest(paths.js))
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js, { sourcemaps: '.' }));
}

function vendor() {
  const out = paths.app + "/static/vendor/";
  return src(npmdist(), { base: "./node_modules" })
    .pipe(rename(function (path) {
      path.dirname = path.dirname.replace(/\/dist/, '').replace(/\\dist/, '');
    }))
    .pipe(dest(out));
};

// Watch
function watchPaths() {
  watch(`${paths.sass}/*.scss`, styles);
  watch(`${paths.templates}/**/*.html`).on('change', reload);
  watch([`${paths.js}/*.js`, `!${paths.js}/*.min.js`], scripts).on(
    'change',
    reload,
  );
}

// Generate all assets
const build = parallel(styles, scripts, vendorScripts, vendor);

// Set up dev environment
const dev = parallel(watchPaths);

task('default', series(build, dev));
task('build', build);
task('dev', dev);
