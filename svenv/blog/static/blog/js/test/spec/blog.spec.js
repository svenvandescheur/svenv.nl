jasmine.getFixtures().fixturesPath = 'svenv/blog/static/blog/js/test/fixtures';


describe('View', function() {
    beforeEach(function() {
        loadFixtures('default.html');
    });

    it('should return a CategoryView when body has class "categoryview"', function() {
        $('body').removeClass();
        $('body').addClass('categoryview');
        baseView = new View();
        view = baseView.getView();
        expect(view.__proto__).toEqual(new CategoryView().__proto__)
    })

    it('should return a PostView when body has class "pageview"', function() {
        $('body').removeClass();
        $('body').addClass('pageview');
        baseView = new View();
        view = baseView.getView();
        expect(view.__proto__).toEqual(new PostView().__proto__)
    })
});

