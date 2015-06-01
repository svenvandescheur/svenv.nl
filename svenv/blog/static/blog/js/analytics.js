/**
 * Svenv.nl Google Analytics handler
 * Provides client-side analytics logic
 */


/**
 * Logic for Google Analytics
 */
function Analytics() {
    /**
     * Wrapper to setup tracking
     * @returns {Object} fluent interface
     */
    this.setUpTracking = function() {
        this.googleAnalytics();

        return this;
    };

    /**
     * Creates the Google Analytics cookie
     * @returns {Object} fluent interface
     */
    this.googleAnalytics = function() {
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

        ga('set', 'anonymizeIp', true);
        ga('create', 'UA-58919715-1', 'auto');
        ga('send', 'pageview');

        return this;
    };
}

/**
 * Provides main routine, called on ready
 */
function analytics() {
    var analytics = new Analytics();
    analytics.setUpTracking();
}

/**
 * Calls main routine
 */
$(document).ready(function () {
    'use strict';
    analytics();
});