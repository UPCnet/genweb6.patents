module.exports = function (grunt) {
    'use strict';

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        compass: {
            css: {
                options: {
                    sassDir: 'scss/',
                    cssDir: 'stylesheets/',
                }
            }
        },
        concat: {
            options: {
                separator: '',
            },
            css: {
                src: ['stylesheets/theme.css'],
                dest: 'stylesheets/theme-concat.css',
            },
            js: {
                src: ['js/main/*.js'],
                dest: 'js/theme-concat.js',
            }
        },
        cssmin: {
            css: {
                src: ["stylesheets/theme-concat.css"],
                dest: "stylesheets/theme-patents.min.css",
            }
        },
        watch: {
            css: {
                files: [
                    'scss/*'
                ],
                tasks: ['compass:css', 'concat:css', 'cssmin:css']
            },
            js: {
                //     files: [
                //         'js/main/*'
                //     ],
                //     tasks: ['concat:js', 'uglify:mainjs']
                files: [
                    'js/widgets/*'
                ],
                tasks: ['uglify:js']
            },

        },
        uglify: {
            js: {
                files: {
                    'js/widget-maxlengthtext.min.js': 'js/widgets/maxlengthtext.js',
                }
            },
            // mainjs: {
            //     files: {
            //         'js/theme-patents.min.js': 'js/theme-concat.js'
            //     }
            // }

        },
        browserSync: {
            plone: {
                bsFiles: {
                    src: [
                        'stylesheets/*.css'
                    ]
                },
                options: {
                    watchTask: true,
                    debugInfo: true,
                    proxy: "localhost:8080/Plone",
                    reloadDelay: 3000,
                    // reloadDebounce: 2000,
                    online: true
                }
            }
        }
    });

    // grunt.loadTasks('tasks');
    // grunt.loadNpmTasks('grunt-browser-sync');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    // CWD to theme folder
    grunt.file.setBase('./src/genweb6/patents/theme');

    // Registered tasks: grunt watch
    grunt.registerTask('default', ["browserSync:plone", "watch"]);
    grunt.registerTask('bsync', ["browserSync:html", "watch"]);
    grunt.registerTask('plone-bsync', ["browserSync:plone", "watch"]);
    grunt.registerTask('minify', ["uglify:js"]);
};
