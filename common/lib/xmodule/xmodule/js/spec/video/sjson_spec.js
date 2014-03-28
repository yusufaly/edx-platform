(function (requirejs, require, define, undefined) {

require(
['video/00_sjson.js'],
function (Sjson) {
    describe('Sjson', function () {
        var data = {
                start: [1, 2, 3],
                text: ['1', '2', '3']
            },
            list = [270, 2720, 5430];

        it ('returns captions', function () {
            var sjson = Sjson(data);
            expect(sjson.getCaptions()).toEqual(data.text);
        });

        it ('returns start times', function () {
            var sjson = Sjson(data);
            expect(sjson.getStartTimes()).toEqual(data.start);
        });

        it ('returns correct length', function () {
            var sjson = Sjson(data);
            expect(sjson.getSize()).toEqual(data.text.length);
        });
    });
});


}(RequireJS.requirejs, RequireJS.require, RequireJS.define));
