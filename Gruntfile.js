module.exports = function (grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    karma: {
      unit: {
        options: {
            configFile: 'karma.conf.js'
        }
      }
    },

    less: {
      build: {
        options: {
          compress: true,
          yuicompress: true,
          optimization: 2
        },
        files: {
          'svenv/blog/static/blog/css/svenv.min.css': ['svenv/blog/static/blog/less/main.less', 'svenv/blog/static/blog/css/fruity.css', 'svenv/blog/static/blog/css/font-awesome.min.css'],
        }
      }
    },

    uglify: {
      options: {
        banner: '/*! Generated: <%= grunt.template.today("yyyy-mm-dd HH:MM:ss") %> */\n'
      },
      build: {
        src: [
          'svenv/blog/static/blog/jquery/dist/jquery.min.js',
          'svenv/blog/static/blog/js/blog.js',
          'svenv/blog/static/blog/js/analytics.js',
        ],
        dest: 'svenv/blog/static/blog/js/svenv.min.js'
      }
    },

    jshint: {
      options: {
        curly: true,
        eqeqeq: false,  // for Google code
        eqnull: true,
        browser: true,
        globals: {
          jQuery: true
        },
        esnext: true,
      },
      all: [
        '*.js',
        '*.json',
        'svenv/blog/static/blog/js/**/*.js',
        '!svenv/blog/static/blog/js/*.min.js',
      ]
    },
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-karma');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.registerTask('default', 'build');
  grunt.registerTask('test', ['jshint', 'jasmine']);
  grunt.registerTask('build', ['copy:build', 'less:build', 'uglify:build']);
};
