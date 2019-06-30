var gulp = require('gulp');
var del = require('del');

var browserify = require('browserify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');

var sass = require('gulp-sass');
sass.compiler = require('node-sass');
var autoprefixer = require('gulp-autoprefixer');
var uglifyCSS = require('gulp-clean-css');

function clean(cb) {
    del(['dist/**']);

    cb();
}

function processJS(cb) {
    browserify('src/js/index.js')
        .transform('babelify', {
            presets: [
                [
                    '@babel/preset-env',
                    {
                        targets: 'last 2 major versions'
                    }
                ]
            ]
        })
        .bundle()
        .pipe(source('main.js'))
        .pipe(buffer())
        .pipe(uglify())

        .pipe(gulp.dest('dist/js'));

    cb();
}

function processSCSS(cb) {
    gulp.src('src/scss/style.scss')
        .pipe(sass({
            outputStyle: 'compressed'
        }))
        .pipe(autoprefixer('last 2 version'))
        .pipe(uglifyCSS())
        .pipe(gulp.dest('dist/css'));

    cb();
}

function processSpinner(cb) {
    gulp.src('src/scss/spinner-show.scss')
        .pipe(sass({
            outputStyle: 'compressed'
        }))
        .pipe(autoprefixer('last 2 version'))
        .pipe(uglifyCSS())
        .pipe(gulp.dest('dist/css'));

    cb();
}

function copyIcons(cb) {
    gulp.src('src/icons/*')
        .pipe(gulp.dest('dist/icons'));

    cb();
}

function copyImages(cb) {
    gulp.src('src/img/*')
        .pipe(gulp.dest('dist/img'));

    cb();
}

function watch(cb) {
    gulp.watch('src/js/*', processJS);
    gulp.watch('src/scss/*', processSCSS);

    cb();
}

exports.clean = gulp.series(clean);
exports.js = gulp.series(processJS);
exports.scss = gulp.series(processSCSS);
exports.spinner = gulp.series(processSpinner);
exports.icons = gulp.series(copyIcons);
exports.img = gulp.series(copyImages);
exports.build = gulp.series(processJS, processSCSS, processSpinner, copyIcons, copyImages);
exports.default = gulp.series(clean, processJS, processSCSS, processSpinner, copyIcons, copyImages);
exports.watch = gulp.series(clean, processJS, processSCSS, processSpinner, copyIcons, copyImages, watch);
