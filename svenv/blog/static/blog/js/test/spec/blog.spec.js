import {View, CategoryView, Navbar, PostView} from '../../blog.js';


jasmine.getFixtures().fixturesPath = 'svenv/blog/static/blog/js/test/fixtures';


describe('View', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
        this.window = window;
    });

    it('should return a CategoryView when body has class "categoryview"', function() {
        $('body').addClass('categoryview');
        var view = new View(),
            currentView = view.getView();
        expect(currentView.constructor.name).toBe('CategoryView');
    });

    it('should return a PostView when body has class "pageview"', function() {
        $('body').addClass('categoryview');
        var view = new View(),
            currentView = view.getView();
        expect(currentView.constructor.name).toBe('CategoryView');
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
        view.setPage(1);  // required due to test runner
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=date&page=2');
        expect($('body').text()).toContain('ajaxtest');
    });

    it('should load the correct page when clicking "Load more"', function() {
        var view = new CategoryView();
        spyOn($, "ajax");
        view.setPage(2);
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=date&page=3');
    });

    it('should show a message when no more posts are available', function() {
        var view = new CategoryView();
        spyOn($, "ajax").and.callFake(function(options) {
            options.error();
        });
        view.setPage(1);  // required due to test runner
        view.fetch_button.click();
        expect($.ajax.calls.mostRecent().args[0].url).toBe('/api/posts/?format=html&ordering=date&page=2');
        expect($('body').text()).toContain('No more posts');
    });

    it('should redirect to the article when left-clicking on it', function() {
        let view = new CategoryView(),
            event = jQuery.Event('click', {'which': 1});

        spyOn(view, 'redirectToArticle');
        $('article:first-child').trigger(event);
        expect(view.redirectToArticle).toHaveBeenCalled();
    });

    it('should redirect to the article when middle-clicking on it', function() {
        let view = new CategoryView(),
            event = jQuery.Event('click', {'which': 2});

        spyOn(view, 'redirectToArticle');
        $('article:first-child').trigger(event);
        expect(view.redirectToArticle).not.toHaveBeenCalled();
    });

    it('should redirect to the article when right-clicking on it', function() {
        let view = new CategoryView(),
            event = jQuery.Event('click', {'which': 3});

        spyOn(view, 'redirectToArticle');
        $('article:first-child').trigger(event);
        expect(view.redirectToArticle).not.toHaveBeenCalled();
    });
});

describe('Navbar', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
    });

    it('should hide the navigation for mobile on search input focusin', function() {
        var navbar = new Navbar();
        navbar.search_input.focusin();
        expect(navbar.nav).toHaveClass('hide-mobile');
    });

    it('should show the navigation for mobile on search input focusout', function() {
        spyOn(window, 'setTimeout').and.callFake(function(callback) {
            callback();
        });
        var navbar = new Navbar();
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
        var navbar = new Navbar();
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
        $('body').removeClass();
        $('body').addClass('postview');
        new PostView();
        expect($('script[src="//svenv.disqus.com/embed.js"]').length).toBe(1);
    });
});
