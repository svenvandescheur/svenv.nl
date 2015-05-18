module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! Generated: <%= grunt.template.today("yyyy-mm-dd HH:MM:ss") %> */\n'
      },
      build: {
        src: [
          'svenv/blog/static/blog/js/jquery.min.js',
          'svenv/blog/static/blog/vendor/less/less.min.js',
          'svenv/blog/static/blog/js/blog.js',
          'svenv/blog/static/blog/js/cookiecontrol.js',
          'svenv/blog/static/blog/js/run_prettify.js'
        ],
        dest: 'svenv/blog/static/blog/js/svenv.min.js'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.registerTask('default', ['uglify']);
};