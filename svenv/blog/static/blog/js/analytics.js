'use strict';

import $ from 'jquery';


/**
 * Logic for Google Analytics
 */
export default class Analytics {
    /**
     * Wrapper to setup tracking
     * Check if user is expected to be a visitor first
     * @returns {Object} fluent interface
     */
    constructor() {
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
    isVisitor() {
        this.checkNonVisitorParam();

        if ($('body').data('dnt') === 'True') {
            return false;
        }

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
    checkNonVisitorParam() {
        var queryString = this.getQueryString();
        if(queryString.match('nv=') && typeof(Storage) !== "undefined") {
            localStorage.setItem("analytics.noVisitor", true);
        }
    };

    /**
     * Gets the query string of the request
     * @param {string} The query string
     */
     getQueryString() {
        return window.location.search;
     };

    /**
     * Fires Google Tag Manager
     * @returns {Object} fluent interface
     */
    googleTagManager() {
        (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        '//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-KW29N3');
    };
}
