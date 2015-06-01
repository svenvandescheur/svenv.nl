/**
 * Blog javascript file
 * Provides dynamic interaction on frontend
 */


/**
 * Logic common for all views
 */
function View() {
    'use strict';
    this.prettyprint_target = $('code');

    /**
     * Finds the current view
     * @returns {string} The current view
     */
    this.getView = function () {
        if ($('body').hasClass('categoryview')) {
            return 'categoryview';
        }

        if ($('body').hasClass('postview')) {
            return 'postview';
        }
    };
}

/**
 * Provides methods for categoryview
 */
function CategoryView() {
    'use strict';
    this.api_url = '/api/';
    this.content_section = $('section#content');
    this.fetch_button = $('.fetch_posts');

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
        $(data).insertBefore(this.fetch_button).hide().fadeIn();
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
}

/**
 * Provides methods for postview
 */
function PostView () {
    'use strict';
    this.disqus_shortname = 'svenv';

    /**
     * Add Disqus to the current page
     * @returns {Object} fluent interface
     */
    this.disqus = function () {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = '//' + this.disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        return this;
    }
}

/**
 * Provides main routine, called on ready
 */
function blog() {
    'use strict';
    // Get base view
    var view = new View(),
        viewClass = view.getView();

    // view specific logic
    if (viewClass === 'categoryview') {
        var categoryView = new CategoryView();

        categoryView.fetch_button.click(function (e) {
            e.preventDefault();
            categoryView.fetchPosts();
        });
    } else if (viewClass === 'postview') {
        var postView = new PostView();
        postView.disqus();
    }
}

/**
 * Calls main routine
 */
$(document).ready(function () {
    'use strict';
    blog();
});