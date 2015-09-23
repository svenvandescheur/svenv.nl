jasmine.getFixtures().fixturesPath = 'svenv/blog/static/blog/js/test/fixtures';


describe('Analytics', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
    });

    it('should receive a call to the constructor when the document is ready', function() {
        var called = false,
            oldAnalytics = Analytics;
        Analytics = jasmine.createSpy().and.callFake(function () {
            this.construct = function() {
                called = true;
            };
        });
        analytics();
        expect(called).toBeTruthy();
        Analytics = oldAnalytics;
    });

    it('should set the analytics.noVisitor property in localstoreage', function() {
        var a = new Analytics();
        spyOn(localStorage, 'setItem').and.callThrough();
        a.construct();
        expect(a.isVisitor()).toBeTruthy();
        spyOn(a, 'getQueryString').and.returnValue('?nv=tue');
        a.construct();
        expect(localStorage.setItem).toHaveBeenCalledWith('analytics.noVisitor', true);
        expect(a.isVisitor()).toBeFalsy();
    });
});
