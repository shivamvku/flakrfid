var gulp = require('gulp')
    , uglify = require('gulp-uglify')
    , concat = require('gulp-concat')
    , inject = require('gulp-inject')
    , angularFilesort = require('gulp-angular-filesort');


gulp.task('html:copy', function () {
    return gulp.src('./build/administration/*/*.html').pipe(gulp.dest('./static/html/'))
});

gulp.task('styles:inject', function () {
    var target = gulp.src('./static/index.html');
    var sources = gulp.src([
        './static/vendor/bootstrap-css-only/css/bootstrap.min.css',
        './static/vendor/angular-bootstrap/ui-bootstrap-csp.css',
        './static/css/site.css'
    ], {read: false});

    return target
        .pipe(inject(sources, {addRootSlash: false}))
        .pipe(gulp.dest('./static/'))
});

gulp.task('app-scripts:compile', function () {
    return gulp.src(['./build/administration/*.js', './build/administration/*/*.js'])
        .pipe(angularFilesort())
        .pipe(concat('administration.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./static/js/'));
});

gulp.task('scripts:inject', ['app-scripts:compile'], function () {
    var sources = [
        './static/vendor/angular/angular.min.js',
        './static/vendor/angular-route/angular-route.min.js',
        './static/vendor/angular-bootstrap/ui-bootstrap.min.js',
        './static/vendor/angular-bootstrap/ui-bootstrap-tpls.min.js',
        './static/vendor/ng-file-upload/ng-file-upload.min.js',
        './static/vendor/ng-file-upload-shim/ng-file-upload-shim.min.js',
        './static/vendor/angular-cookies/angular-cookies.js',
        './static/js/administration.min.js'];

    return gulp.src('./static/index.html')
        .pipe(inject(gulp.src(sources), {addRootSlash: false}))
        .pipe(gulp.dest('./static/'));
});

gulp.task('static:build', ['scripts:inject', 'styles:inject'], function () {
});