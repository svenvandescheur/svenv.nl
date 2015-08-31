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
    this.setUpTracking = function() {
        if (this.isVisitor()) {
            this.googleTagManager();
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
    new Analytics().setUpTracking();
}

/**
 * Calls main routine
 */
$(document).ready(function () {
    'use strict';
    analytics();
});