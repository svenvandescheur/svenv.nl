/**
 * Svenv.nl Google Analytics handler
 * Provides client-side analytics logic
 */


/**
 * Logic for Google Analytics
 */
function Analytics() {
    'use strict';
    /**
     * Wrapper to setup tracking
     * Check if user is expected to be a visitor first
     * @returns {Object} fluent interface
     */
    this.setUpTracking = function() {
        if (this.isVisitor()) {
            this.googleAnalytics();
        }

        return this;
    };

    /**
     * Returns whether the user is expected to be a visitor
     * @returns {boolean}
     */
    this.isVisitor = function() {
        if(typeof(Storage) !== "undefined") {
            return localStorage.getItem("analytics.noVisitor") !== 'true';
        } else {
            return true;
        }
    }

    /**
     * Creates the Google Analytics cookie
     * @returns {Object} fluent interface
     */
    this.googleAnalytics = function() {
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

        ga('create', 'UA-58919715-1', 'auto');
        ga('require', 'linkid', 'linkid.js');
        ga('set', 'anonymizeIp', true);
        ga('send', 'pageview');

        return this;
    };
}

/**
 * Provides main routine, called on ready
 */
function analytics() {
    'use strict';
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