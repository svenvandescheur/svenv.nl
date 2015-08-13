module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    copy: {
      main: {
        files: [
          {
            src: 'node_modules/jquery/dist/jquery.min.js',
            dest: 'svenv/blog/static/blog/js/jquery.min.js',
          },
          {
            src: 'node_modules/jasmine/lib/jasmine.js',
            dest: 'svenv/blog/static/blog/js/jasmine.js',
          },
          {
            src: 'node_modules/jasmine-jquery/lib/jasmine-jquery.js',
            dest: 'svenv/blog/static/blog/js/jasmine-jquery.js',
          },
        ]
      }
    },

    less: {
      production: {
        options: {
          compress: true,
          yuicompress: true,
          optimization: 2
        },
        files: {
          'svenv/blog/static/blog/css/svenv.min.css': ['svenv/blog/static/blog/less/main.less', 'svenv/blog/static/blog/css/fruity.css'],
        }
      }
    },

    uglify: {
      options: {
        banner: '/*! Generated: <%= grunt.template.today("yyyy-mm-dd HH:MM:ss") %> */\n'
      },
      build: {
        src: [
          'svenv/blog/static/blog/js/jquery.min.js',
          'svenv/blog/static/blog/js/blog.js',
          'svenv/blog/static/blog/js/analytics.js',
        ],
        dest: 'svenv/blog/static/blog/js/svenv.min.js'
      }
    },
  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.registerTask('default', ['copy', 'less', 'uglify']);
};