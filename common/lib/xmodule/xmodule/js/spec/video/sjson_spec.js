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

        it ('Array is converted successfully', function () {
            var sjson = Sjson(data),
                newSpeed = 1.5,
                convertedList;

            runs(function () {
                sjson.convert(newSpeed).done(function (result) {
                    convertedList = result;
                });
            });

            waitsFor(function () {
                return convertedList;
            }, 'Array processing takes too much time', WAIT_TIMEOUT);

            runs(function () {
                expect(convertedList).toEqual([1.5, 3, 4.5]);
            });
        });

        it ('returns captions', function () {
            var sjson = Sjson(data);
            expect(sjson.getCaptions()).toEqual(data.text);
        });

        it ('returns start times', function () {
            var sjson = Sjson(data);
            expect(sjson.getStartTimes()).toEqual(data.start);
        });

        it ('sets default speed', function () {
            var sjson = Sjson(data),
                newSpeed = 1.5,
                convertedList;

            runs(function () {
                sjson.setSpeed(newSpeed).done(function (result) {
                    convertedList = result;
                });
            });

            waitsFor(function () {
                return convertedList;
            }, 'Array processing takes too much time', WAIT_TIMEOUT);

            runs(function () {
                expect(convertedList).toEqual([1.5, 3, 4.5]);
                expect(sjson.getStartTimes()).toEqual([1.5, 3, 4.5]);
            });
        });
    });
});


}(RequireJS.requirejs, RequireJS.require, RequireJS.define));
