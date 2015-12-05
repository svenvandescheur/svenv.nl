jasmine.getFixtures().fixturesPath = 'svenv/blog/static/blog/js/test/fixtures';


describe('View', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
        this.window = window;
    });

    it('should receive a call to getView when the document is ready', function() {
        var called = false,
            oldView = View;
        View = jasmine.createSpy().and.callFake(function () {
            this.getView = function() {
                called = true;
            };
        });
        blog();
        expect(called).toBeTruthy();
        View = oldView;
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
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=date&page=2');
        expect($('body').text()).toContain('ajaxtest');
    });

    it('should load the correct page when clicking "Load more"', function() {
        var view = new CategoryView();
        spyOn($, "ajax");
        view.construct();
        view.setPage(2);
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=date&page=3');
    });

    it('should show a message when no more posts are available', function() {
        var view = new CategoryView();
        spyOn($, "ajax").and.callFake(function(options) {
            options.error();
        });
        view.construct();
        view.setPage(1);  // required due to test runner
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=date&page=2');
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

describe('Navbar', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
    });

    it('should hide the navigation for mobile on search input focusin', function() {
        var navbar = new NavBar();
        navbar.search_input.focusin();
        expect(navbar.nav).toHaveClass('hide-mobile');
    });

    it('should show the navigation for mobile on search input focusout', function() {
        spyOn(window, 'setTimeout').and.callFake(function(callback) {
            callback();
        });
        var navbar = new NavBar();
        navbar.nav.addClass('hide-mobile');
        navbar.search_input.focusout();
        expect(navbar.nav).not.toHaveClass('hide-mobile');
    });

    it('should provide search', function() {
        spyOn(window, 'setTimeout').and.callFake(function(callback) {
            callback();
        });
        spyOn($, 'ajax').and.callFake(function(options) {
            options.success('<article><header><a href="/unixandlinux/dockerclean"><img src="https://svenv.nl/media/2015/05/21/docker.png" width="450" height="300" alt="Docker logo"></a></header> <section><h2><a href="/unixandlinux/dockerclean">Cleaning up a full Docker partition</a></h2><p>search test</p></section></article>');
        });
        var navbar = new NavBar();
        navbar.search_input.val('docker').trigger('input');
        expect(window.setTimeout).toHaveBeenCalled();
        expect($('body').text()).toContain('search test');
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
