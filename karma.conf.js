/* global module */
module.exports = function (config) {
    'use strict';
    config.set({
        autoWatch: true,
        singleRun: true,
        browsers: ['PhantomJS'],
        frameworks: ['jspm', 'jasmine-jquery', 'jasmine', 'es6-shim'],
        reporters: ['spec'],

        jspm: {
            config: 'config.js',
            loadFiles: [
                'svenv/blog/static/blog/js/test/spec/*.spec.js',
            ],
            serveFiles: [
                'jspm_packages/',
                'svenv/blog/static/blog/js/*.js',
                'svenv/blog/static/blog/js/test/fixtures/*',
            ]
        },

        proxies: {
            '/jspm_packages/': '/base/jspm_packages/',
            '/svenv': '/base/svenv',
        },
    });
};