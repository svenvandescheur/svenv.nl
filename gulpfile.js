var gulp = require('gulp'),
    Server = require('karma').Server,
    jshint = require('gulp-jshint'),
    gulp_jspm = require('gulp-jspm'),
    rename = require("gulp-rename");
    uglify = require('gulp-uglify')
    less = require('gulp-less'),
    nano = require('gulp-cssnano'),
    concatCss = require('gulp-concat-css');


/**
 * Run Javascript unit tests
 */
gulp.task('test-js', function (done) {
  new Server({
    configFile: __dirname + '/karma.conf.js',
    singleRun: true
  }, done).start();
});


/**
 * Lint JavaScript
 */
gulp.task('lint-js', function() {
  return gulp.src(['./svenv/blog/static/blog/**/*.js', '!./svenv/blog/static/blog/js/svenv.*'])
    .pipe(jshint({
        'bitwise': true,
        'curly': true,
        'eqeqeq': true,
        'esversion': 6,
        'forin': true,
        'freeze': true,
        'futurehostile': true,
        'maxdepth': 2,
        'maxstatements': 15,
        'undef': true,
        'unused': true,

        'devel': true,  // We want to use console.log and don't support legacy IE
        'jasmine': true,
        'jquery': true,
        browser: true,
      }))
    .pipe(jshint.reporter('default'))
});


/**
 * Bundle JavaScript into a single file
 */
gulp.task('bundle-js', function(){
    return gulp.src('./svenv/blog/static/blog/js/blog.js')
        .pipe(gulp_jspm({'selfExecutingBundle': true}))
        .pipe(rename({'basename': 'svenv'}))
        .pipe(gulp.dest('./svenv/blog/static/blog/js/'));
});


/**
 * Minify JavaScript
 */
gulp.task('minify-js', ['bundle-js'], function() {
  return gulp.src('svenv/blog/static/blog/js/svenv.js')
    .pipe(uglify())
    .pipe(rename({'extname': '.min.js'}))
    .pipe(gulp.dest('svenv/blog/static/blog/js/'));
});


/**
 * Compile LESS
 */
gulp.task('compile-less', function () {
    return gulp.src('./svenv/blog/static/blog/less/main.less')
    .pipe(less())
    .pipe(gulp.dest('./svenv//blog/static/blog/css/'));
});


/**
 * Merge CSS
 */
gulp.task('merge-css', ['compile-less'], function () {
    return gulp.src(['./svenv/blog/static/blog/css/*.css', 'jspm_packages/npm/font-awesome*/css/font-awesome.min.css'])
    .pipe(concatCss('./svenv/blog/static/blog/css/svenv.min.css'))
    .pipe(gulp.dest('./'));
});


/**
 * Minify CSS
 */
gulp.task('minify-css', ['merge-css'], function() {
    return gulp.src('./svenv/blog/static/blog/css/svenv.min.css')
        .pipe(nano())
        .pipe(gulp.dest('./svenv//blog/static/blog/css/'));
});


/**
 * Setup aliasses
 */
gulp.task('test', ['lint-js', 'test-js']);
gulp.task('build-js', ['minify-js']);
gulp.task('build-css', ['minify-css']);
gulp.task('build', ['build-js', 'build-css']);


/**
 * By default, test and build
 */
gulp.task('default', ['test', 'build']);