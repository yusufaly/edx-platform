(function (requirejs, require, define, undefined) {

require(
['video/00_sjson.js'],
function (Sjson) {
    describe('Sjson', function () {
        var data = {
            start: [270, 2720, 5430],
            end: [2720, 5430, 7160],
            text: [
                "Hi, welcome to Edx.",
                "As you know, our courses are entirely online.",
                "So before we start learning about the subjects that"
            ]
        };

        it ('Array is processed successfully', function () {
            var convertedData;

            runs(function () {
                var oldSpeed = 1,
                    newSpeed = 2;

                Sjson.convert(data, oldSpeed, newSpeed).done(function (result) {
                    convertedData = result;
                });
            });

            waitsFor(function () {
                return convertedData;
            }, 'Array processing takes too much time', WAIT_TIMEOUT);

            runs(function () {
                expect(convertedData).toEqual({
                    start: [540, 5440, 10860],
                    end: [5440, 10860, 14320],
                    text: [
                        "Hi, welcome to Edx.",
                        "As you know, our courses are entirely online.",
                        "So before we start learning about the subjects that"
                    ]
                });
            });
        });
    });
});


}(RequireJS.requirejs, RequireJS.require, RequireJS.define));
