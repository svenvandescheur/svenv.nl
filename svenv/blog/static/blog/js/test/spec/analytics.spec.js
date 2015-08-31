jasmine.getFixtures().fixturesPath = 'svenv/blog/static/blog/js/test/fixtures';


describe('AnalyticsTest', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
    });

    it('should call the constructor when the document is ready', function() {
        var called = false;
        Analytics = jasmine.createSpy().and.callFake(function () {
            this.construct = function() {
                called = true;
            };
        });
        analytics();
        expect(called).toBeTruthy();
    });
});
