/**
 * Blog javascript file
 * Provides dynamic interaction on frontend
 */


/**
 * Logic common for all views
 */
function View() {
    this.prettyprint_target = $('code');

    /**
     * Finds the current view
     * @returns {String} The current view
     */
    this.getView = function() {
        if ($('body').hasClass('listview')) {
            return 'listview';
        };

        if ($('body').hasClass('postview')) {
            return 'postview';
        };
    }

    /**
     * Sets up pretty printing for code
     * @returns {Object} fluent interface
     */
    this.prettyPrint = function() {
        this.prettyprint_target.addClass('prettyprint');
        return this;
    };
};

/**
 * Provides methods for ListView
 */
function ListView() {
    this.api_url = '/api/';
    this.content_section = $('section#content');
    this.fetch_button = $('.fetch_posts');

    /**
     * Fetches additional posts
     * @param {Number} page The page to load data from
     * @returns {Object} fluent interface
     */
    this.fetchPosts = function(page) {
        self = this;
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
    this._fetchPostsSuccess = function(data) {
        $(data).insertBefore(this.fetch_button).hide().fadeIn();
        this.setPage(this.nextPage());
    };

   /**
     * Error callback for fetchPosts
     * notifies the user that fetching posts has failed
     */
    this._fetchPostsError = function() {
        this.fetch_button.text('No more posts.');
    };

    /**
     * Calculates the next page
     * @returns {Number} The next page
     */
    this.nextPage = function() {
        return this.getPage() + 1;
    };

    /**
     * Gets the current page
     * @returns {Number} the current page
     */
    this.getPage = function() {
        return parseInt($('body').attr('data-page'))
    };

    /**
     * Sets the current page
     * @param {Number} page The new page value
     * @returns {Object} fluent interface
     */
    this.setPage = function(page) {
        $('body').attr('data-page', page);
        return this;
    };
};

/**
 * Provides main routine, called on ready
 */
function main() {
    // Get base view
    view = new View;
    viewClass = view.getView();

    // Prettyprint
    view.prettyPrint();

    // Listview specific logic
    if (viewClass == 'listview') {
        listView = new ListView;

        listView.fetch_button.click(function(e) {
            e.preventDefault();
            listView.fetchPosts();
        });
    };
};

/**
 * Calls main routine
 */
$(document).ready(function() {
    main();
});