module.exports = function (grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    copy: {
      build: {
        files: [{
            expand: true,
            cwd: 'node_modules/',
            src: '*/**',
            dest: 'svenv/blog/static/blog/',
          }, {
            expand: true,
            cwd: 'svenv/blog/static/blog/font-awesome/',
            src: ['css/font-awesome.min.css', 'fonts/*'],
            dest: 'svenv/blog/static/blog/',
          },

        ]
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
      all: ['Gruntfile.js', 'svenv/blog/static/blog/js/*.js', '!svenv/blog/static/blog/js/*.min.js']
    },

    jasmine: {
      analytics: {
        src: 'svenv/blog/static/blog/js/analytics.js',
        options: {
          vendor: [
            'svenv/blog/static/blog/jquery/dist/jquery.min.js',
            'svenv/blog/static/blog/jasmine-jquery/lib/jasmine-jquery.js'
          ],
          specs: 'svenv/blog/static/blog/js/test/spec/analytics.spec.js',

        }
      },
      blog: {
        src: 'svenv/blog/static/blog/js/blog.js',
        options: {
          vendor: [
            'svenv/blog/static/blog/jquery/dist/jquery.min.js',
            'svenv/blog/static/blog/jasmine-jquery/lib/jasmine-jquery.js'
          ],
          specs: 'svenv/blog/static/blog/js/test/spec/blog.spec.js',

        }
      },
    },
  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-jasmine');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.registerTask('default', 'build');
  grunt.registerTask('test', ['jshint', 'jasmine']);
  grunt.registerTask('build', ['copy:build', 'less:build', 'uglify:build']);
};
