/**
 * Svenv.nl Google Tag Manager handler
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
    this.construct = function() {
        if (this.isVisitor()) {
            this.googleTagManager();
        } else {
            console.log('Excluded from analytics.');
        }

        return this;
    };

    /**
     * Returns whether the user is expected to be a visitor
     * @returns {boolean}
     */
    this.isVisitor = function() {
        this.checkNonVisitorParam();

        if(typeof(Storage) !== "undefined") {
            return localStorage.getItem("analytics.noVisitor") !== 'true';
        } else {
            return true;
        }
    };

    /**
     * Checks the GET query string for "nv" (no visitor)
     * If the key is found, set "analytics.noVisitor" to true in localstorage
     */
    this.checkNonVisitorParam = function() {
        var queryString = this.getQueryString();
        if(queryString.match('nv=') && typeof(Storage) !== "undefined") {
            localStorage.setItem("analytics.noVisitor", true);
        }
    };

    /**
     * Gets the query string of the request
     * @param {string} The query string
     */
     this.getQueryString = function() {
        return window.location.search;
     };

    /**
     * Fires Google Tag Manager
     * @returns {Object} fluent interface
     */
    this.googleTagManager = function() {
        (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        '//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-KW29N3');
    };
}

/**
 * Provides main routine, called on ready
 */
function analytics() {
    'use strict';
    new Analytics().construct();
}

/**
 * Calls main routine
 */
$(document).ready(function () {
    'use strict';
    analytics();
});