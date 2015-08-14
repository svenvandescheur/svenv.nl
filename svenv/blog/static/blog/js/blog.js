/**
 * Blog javascript file
 * Provides dynamic interaction on frontend
 */


/**
 * Logic common for all views
 */
function View() {
    'use strict';
    /**
     * Finds the current view
     * @returns {string} The current view
     */
    this.getView = function () {
        if ($('body').hasClass('categoryview')) {
            return new CategoryView();
        }

        if ($('body').hasClass('postview') || $('body').hasClass('pageview')) {
            return new PostView();
        }
    };
}

/**
 * Provides methods for categoryview
 */
function CategoryView() {
    'use strict';
    this.api_url = '/api/';
    this.content_section = $('main');
    this.fetch_button = $('.fetchposts');
    this.articles = this.content_section.find('article');
    this.articleLinkSelector = 'header a';
    this.transitionInterval = 100;

    /**
     * Runs the logic for this view
     * @returns {Object} fluent interface
     */
    this.construct = function () {
        this.setUpFetchPosts()
            .fadeInArticles()
            .setUpRedirectToArticle();

        return this;
    };

    /**
     * Binds the fetch button to fetchPosts()
     * @returns {Object} fluent interface
     */
    this.setUpFetchPosts = function () {
        var self = this;
        this.fetch_button.click(function (e) {
            e.preventDefault();
            self.fetchPosts();
        });

        return this;
    };

    /**
     * Fetches additional posts
     * @returns {Object} fluent interface
     */
    this.fetchPosts = function () {
        var self = this;
        $.ajax({
            url: self.api_url + 'posts/?format=html&ordering=-date&page=' + self.nextPage(),
            success: $.proxy(self._fetchPostsSuccess, self),
            error: $.proxy(self._fetchPostsError, self)
        });

        return this;
    };

    /**
     * Success callback for fetchPosts
     * adds the received data to the dom and update the current page value
     */
    this._fetchPostsSuccess = function (data) {
        $(data).insertBefore(this.fetch_button);

        var nodes = $('article').filter(function() {
            return $(this).css('opacity') !== '1';
        });

        this._fadeIn(nodes);
        this.setPage(this.nextPage());
    };

    /**
     * Error callback for fetchPosts
     * notifies the user that fetching posts has failed
     */
    this._fetchPostsError = function () {
        this.fetch_button.text('No more posts.');
    };

    /**
     * Calculates the next page
     * @returns {number} The next page
     */
    this.nextPage = function () {
        return this.getPage() + 1;
    };

    /**
     * Gets the current page
     * @returns {number} the current page
     */
    this.getPage = function () {
        return parseInt($('body').attr('data-page'), 10);
    };

    /**
     * Sets the current page
     * @param {number} page The new page value
     * @returns {Object} fluent interface
     */
    this.setPage = function (page) {
        $('body').attr('data-page', page);
        return this;
    };

    /**
     * Animates articles fading in using CSS3 transitions
     * @returns {Object} fluent interface
     */
    this.fadeInArticles = function () {
        return this._fadeIn(this.articles);
    };

    /**
     * Animates jQuery selected nodes fading in using CSS3 transitions
     * @param {Object} set of jQuery nodes
     * @returns {Object} fluent interface
     */
    this._fadeIn = function (nodes) {
        var self = this;

        $.each(nodes, function (index) {
            var delay = index * self.transitionInterval;

            $(this).css({  // $(this).transition({
                'opacity': 1,
                'delay': delay
            });
        });

        return this;
    };

    /**
     * Binds articles to redirectToArticle()
     * @returns {Object} fluent interface
     */
    this.setUpRedirectToArticle = function () {
        var self = this;
        this.articles.click(function () {
            self.redirectToArticle($(this));
        });

        return this;
    };

    /**
     * Redirect to the permalink of the article
     * @param {Object} jQuery node
     */
    this.redirectToArticle = function (article) {
        var a = article.find(this.articleLinkSelector);
        window.location = a.attr('href');
    };
}

/**
 * Provides methods for postview
 */
function PostView () {
    'use strict';
    this.disqus_shortname = 'svenv';
    this.article_header_image = $('article header img');
    this.parallax_ratio = 0.3;

    /**
     * Runs the logic for this view
     * @returns {Object} fluent interface
     */
    this.construct = function () {
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
    };

    /**
     * Add Disqus to the current page
     * @returns {Object} fluent interface
     */
    this.disqus = function () {
        if ($('body').hasClass('postview')) {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + this.disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        }

        return this;
    };

    /**
     * Create a parallax effect on the header by utilizing requestAnimationFrame
     * @returns {Object} fluent interface
     */
    this.parallaxHeader = function () {
        var self = this;
        $(window).scroll(function(){
            requestAnimFrame(self._parallaxHeader.bind(self));
        });

        return this;
    };

    /**
     * Sets the parallax position of the header
     * @returns {Object} fluent interface
     */
    this._parallaxHeader = function () {
        this.article_header_image.css({
            'top': this.parallax_ratio * $(window).scrollTop()
        });

        return this;
    };
}

/**
 * Provides main routine, called on ready
 */
function blog() {
    'use strict';
    // Get base view
    var baseView = new View(),
        view = baseView.getView();

    view.construct();
}

/**
 * Calls main routine
 */
$(document).ready(function () {
    'use strict';
    blog();
});
