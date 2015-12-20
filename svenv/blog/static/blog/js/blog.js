import $ from 'jquery';

import Analytics from './analytics';


/**
 * Logic common for all views
 */
class View {
    /**
     * Finds the current view
     * @returns {string} The current view
     */
    getView() {
        if ($('body').hasClass('categoryview')) {
            return new CategoryView();
        }

        if ($('body').hasClass('postview') || $('body').hasClass('pageview')) {
            return new PostView();
        }
    }
}

/**
 * Provides methods for categoryview
 */
class CategoryView {
    /**
     * Runs the logic for this view
     * @returns {CategoryView} fluent interface
     */
    constructor() {
        this.api_url = '/api/';
        this.content_section = $('main');
        this.fetch_button = $('.fetchposts');
        this.fetch_url = this.api_url + 'posts/?format=html&ordering=date';
        this.article_list = this.content_section.find('.articleslist');
        this.articles = this.article_list.find('article');
        this.articleLinkSelector = 'header a';
        this.transitionInterval = 100;

        new NavBar();

        this.setUpFetchPosts()
            .fadeInArticles()
            .setUpRedirectToArticle();

        return this;
    }

    /**
     * Binds the fetch button to fetchPosts()
     * @returns {CategoryView} fluent interface
     */
    setUpFetchPosts() {
        this.setFetchPostsTarget(this.fetch_url);

        var self = this;
        this.fetch_button.click(function (e) {
            e.preventDefault();
            self.fetchPosts();
        });

        return this;
    }

    /**
     * Fetches additional posts
     * @returns {CategoryView} fluent interface
     */
    fetchPosts() {
        var self = this;
        $.ajax({
            url: this.getFetchPostsTarget() + '&page=' + this.nextPage(),
            success: $.proxy(self._fetchPostsSuccess, self),
            error: $.proxy(self._fetchPostsError, self)
        });

        return this;
    }

    /**
     * Gets the api url to fetch posts from
     * @returns {string} The api url
     */
    getFetchPostsTarget() {
        return this.fetch_button.data('fetchTarget');
    }

    /**
     * Gets the api url to fetch posts from
     * @param {string} url The api url
     * @returns {CategoryView} fluent interface
     */
    setFetchPostsTarget(url) {
        this.fetch_button.data('fetchTarget', url);
        return this;
    }

    /**
     * Success callback for fetchPosts
     * adds the received data to the dom and update the current page value
     */
    _fetchPostsSuccess(data) {
        $(data).insertBefore(this.fetch_button);

        var nodes = $('article').filter(function() {
            return $(this).css('opacity') !== '1';
        });

        this._fadeIn(nodes);
        this.setPage(this.nextPage());
    }

    /**
     * Error callback for fetchPosts
     * notifies the user that fetching posts has failed
     */
    _fetchPostsError() {
        this.fetch_button.text('No more posts.');
    }

    /**
     * Calculates the next page
     * @returns {number} The next page
     */
    nextPage() {
        return this.getPage() + 1;
    }

    /**
     * Gets the current page
     * @returns {number} the current page
     */
    getPage() {
        return parseInt($('body').attr('data-page'), 10);
    }

    /**
     * Sets the current page
     * @param {number} page The new page value
     * @returns {CategoryView} fluent interface
     */
    setPage(page) {
        $('body').attr('data-page', page);
        return this;
    }

    /**
     * Animates articles fading in using CSS3 transitions
     * @returns {CategoryView} fluent interface
     */
    fadeInArticles() {
        return this._fadeIn(this.articles);
    }

    /**
     * Animates jQuery selected nodes fading in using CSS3 transitions
     * @param {Object} set of jQuery nodes
     * @returns {CategoryView} fluent interface
     */
    _fadeIn(nodes) {
        var self = this;

        $.each(nodes, function (index) {
            var delay = index * self.transitionInterval;

            $(this).css({  // $(this).transition({
                'opacity': 1,
                'delay': delay
            });
        });

        return this;
    }

    /**
     * Binds articles to redirectToArticle()
     * @returns {CategoryView} fluent interface
     */
    setUpRedirectToArticle() {
        var self = this;
        this.articles.click(function () {
            self.redirectToArticle($(this));
        });

        return this;
    }

    /**
     * Redirect to the permalink of the article
     * @param {Object} jQuery node
     */
    redirectToArticle(article) {
        var a = article.find(this.articleLinkSelector);
        window.location = a.attr('href');
    }

    /**
     * Remove current articles and shows new content
     * @param {Object} data jQuery provided data
     * @returns {CategoryView} fluent interface
     */
    setArticles(data) {
        this.articles.remove();
        this._fetchPostsSuccess(data);
        this.setPage(1);
        return this;
    }
}

/**
 * Provides methods for navbar component
 */
class NavBar {
    /**
     * Runs the logic for this view
     * @returns {Object} fluent interface
     */
    constructor() {
        this.base = $('.navbar');
        this.nav = this.base.find('nav');
        this.search_input = this.base.find('input#search');
        this.search_timeout_duration = 200;
        this.search_url = '/api/search/posts/';

        this.setUpSearchFocusIn()
            .setUpSearchFocusOut()
            .setUpSearchInput();
        return this;
    }

    /**
     * Binds focusin event on search_input to hideNavOnMobile()
     * @returns {NavBar} fluent interface
     */
    setUpSearchFocusIn() {
        this.search_input.on('focusin', $.proxy(this.hideNavOnMobile, this));
        return this;
    }
    /**
     * Adds the hide-mobile class on nav
     * @returns {NavBar} fluent interface
     */
    hideNavOnMobile() {
        this.nav.addClass('hide-mobile');
        return this;
    }

    /**
     * Binds focusout event on search_input to showNavOnMobile()
     * @returns {NavBar} fluent interface
     */
    setUpSearchFocusOut() {
        this.search_input.on('focusout', $.proxy(this.showNavOnMobile, this));
        return this;
    }

    /**
     * Waits 300 microseconds before removing hide-mobile class from nav
     * @returns {NavBar} fluent interface
     */
    showNavOnMobile() {
        var nav = this.nav;
        window.setTimeout(function() {
            nav.removeClass('hide-mobile');
        }, 300);
        return this;
    }

    /**
     * Binds input event on search_input to serach()
     * @returns {NavBar} fluent interface
     */
    setUpSearchInput() {
        this.search_input.on('input', $.proxy(this.search, this));
        return this;
    }

    /**
     * Uses search_timeout mechanism to prevent to many search queries
     * @returns {NavBar} fluent interface
     */
    search() {
        var self = this;
        window.clearTimeout(this.search_timeout);

        this.search_timeout = window.setTimeout(function() {
            self.searchRequest();
        }, this.search_timeout_duration);

        return this;
    }

    /**
     * Searches using ajax
     * @returns {NavBar} fluent interface
     */
    searchRequest() {
        var query = this.search_input.val();

        $.ajax({
            'url': this.search_url,
            'method': 'GET',
            'data': {
                'format': 'html',
                'query': query,
            },
            'success': $.proxy(this.showSearchResults, this, query),
            'error': $.proxy(this.ajaxError, this),
        });

        return this;
    }

    /**
     * Shows the search results
     * @param {Object} data jQuery provided data
     * @returns {NavBar} fluent interface
     */
    showSearchResults(query, data) {
        var categoryview = new CategoryView();
        categoryview.setFetchPostsTarget(categoryview.api_url + 'search/posts/?format=html&query=' + query)
                    .setArticles(data);

        if(!query) {
            categoryview.setFetchPostsTarget(categoryview.fetch_url);
        }

        return this;
    }

    /**
     * Logs an ajax error
     * @returns {NavBar} fluent interface
     */
    ajaxError() {
        console.log('Failed to fetch data');
        return this;
    }
}

/**
 * Provides methods for postview
 */
class PostView {
    /**
     * Runs the logic for this view
     * @returns {Object} fluent interface
     */
    constructor() {
        this.disqus_shortname = 'svenv';
        this.article_header_image = $('article header img');
        this.parallax_ratio = 0.3;

        this.disqus();

        // Universal requestAnimationFrame
        window.requestAnimFrame = (function(){
            return  window.requestAnimationFrame       ||
                window.webkitRequestAnimationFrame ||
                window.mozRequestAnimationFrame    ||
                function (callback){
                    window.setTimeout(callback, 1000 / 60);
                };
        })();

        this.parallaxHeader();
        return this;
    }

    /**
     * Add Disqus to the current page
     * @returns {Object} fluent interface
     */
    disqus() {
        if ($('body').hasClass('postview')) {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + this.disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        }

        return this;
    }

    /**
     * Create a parallax effect on the header by utilizing requestAnimationFrame
     * @returns {Object} fluent interface
     */
    parallaxHeader() {
        var self = this;
        $(window).scroll(function(){
            requestAnimFrame(self._parallaxHeader.bind(self));
        });

        return this;
    }

    /**
     * Sets the parallax position of the header
     * @returns {Object} fluent interface
     */
    _parallaxHeader() {
        this.article_header_image.css({
            'top': this.parallax_ratio * $(window).scrollTop()
        });

        return this;
    }
}

/**
 * Provides main routine, called on ready
 */
function blog() {
    new View().getView();
    new Analytics();
}

/**
 * Calls main routine
 */
$(document).ready(function () {
    'use strict';
    blog();
});
