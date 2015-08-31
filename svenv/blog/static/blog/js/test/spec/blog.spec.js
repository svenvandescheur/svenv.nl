jasmine.getFixtures().fixturesPath = 'svenv/blog/static/blog/js/test/fixtures';


describe('View', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
    });

    it('should return a CategoryView when body has class "categoryview"', function() {
        $('body').removeClass();
        $('body').addClass('categoryview');
        baseView = new View();
        view = baseView.getView();
        expect(view instanceof CategoryView).toBeTruthy();
    });

    it('should return a PostView when body has class "pageview"', function() {
        $('body').removeClass();
        $('body').addClass('pageview');
        baseView = new View();
        view = baseView.getView();
        expect(view instanceof PostView).toBeTruthy();
    });
});

describe('CategoryView', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
    });

    it('should load additional posts when clicking "Load more"', function() {
        var view = new CategoryView();
        spyOn($, "ajax").and.callFake(function(options) {
            options.success('<article>ajaxtest</article>');
        });
        view.construct();
        view.setPage(1);  // required due to test runner
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=-date&page=2');
        expect($('body').text()).toContain('ajaxtest');
    });

    it('should load the correct page when clicking "Load more"', function() {
        var view = new CategoryView();
        spyOn($, "ajax");
        view.construct();
        view.setPage(2);
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=-date&page=3');
    });

    it('should show a message when no more posts are available', function() {
        var view = new CategoryView();
        spyOn($, "ajax").and.callFake(function(options) {
            options.error();
        });
        view.construct();
        view.setPage(1);  // required due to test runner
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=-date&page=2');
        expect($('body').text()).toContain('No more posts');
    });

    it('should redirect to the article when clicking on it', function() {
        var view = new CategoryView();
        spyOn(view, 'redirectToArticle');
        view.construct();
        $('article:first-child').click();
        expect(view.redirectToArticle).toHaveBeenCalled();
    });
});

describe('PostView', function() {
    beforeEach(function() {
        loadFixtures('postview.html');
    });

    it('should load disqus when body has class "postview"', function() {
        var view = new PostView();
        $('body').removeClass();
        $('body').addClass('postview');
        $('script').remove();
        view.construct();
        expect($('script[src="//svenv.disqus.com/embed.js"]').length).toBe(1);
    });
});
