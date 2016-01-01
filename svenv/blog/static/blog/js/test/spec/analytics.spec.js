import {Analytics} from '../../analytics.js'


jasmine.getFixtures().fixturesPath = 'svenv/blog/static/blog/js/test/fixtures';


describe('Analytics', function() {
    beforeEach(function() {
        loadFixtures('categoryview.html');
    });

    it('should set the analytics.noVisitor property in localstoreage', function() {
        var a = new Analytics();
        spyOn(a, 'getQueryString').and.returnValue('?nv=tue');
        spyOn(a, 'isVisitor').and.callThrough();
        spyOn(localStorage, 'setItem').and.callThrough();
        a.isVisitor();
        expect(localStorage.setItem).toHaveBeenCalledWith('analytics.noVisitor', true);
        expect(a.isVisitor()).toBeFalsy();
    });
});
