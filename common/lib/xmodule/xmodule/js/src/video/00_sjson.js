(function (requirejs, require, define) {

define(
'video/00_sjson.js',
['video/00_process.js'],
function(Process) {
"use strict";

    var ProcessAdapter = (function () {
        var process = function (oldSpeed, newSpeed) {
            return function (value) {
                return value * newSpeed / oldSpeed;
            };
        };

        return {
            convert: function (list, oldSpeed, newSpeed) {
                return Process.array(list, process(oldSpeed, newSpeed));
            }
        };
    }());

    var Sjson = function (data) {
        var converter = ProcessAdapter,
            sjson = {
                start: data.start.concat(),
                text: data.text.concat()
            },
            etalon_times = sjson.start,
            cache = {},
            module = {};

        var getter = function (propertyName) {
            return function () {
                return sjson[propertyName];
            };
        };

        var convert = function (newSpeed) {
            var list = etalon_times,
                speed = Number(newSpeed);

            if (cache[speed]) {
                return $.Deferred().resolve(cache[speed]).promise();
            }

            return converter.convert(list, 1, speed).done(function (list) {
                updateCache(speed, list);
            });
        };

        var updateCurrentTimes = function (list) {
            sjson.start = list;
        };

        var updateCache = function (speed, list) {
            cache[speed] = list;
        };

        updateCache(1, sjson.start);

        return {
            convert: convert,
            setSpeed: function (speed) {
                return convert(speed).done(updateCurrentTimes);
            },
            getCaptions: getter('text'),
            getStartTimes: getter('start'),
        };
    };

    return Sjson;
});
}(RequireJS.requirejs, RequireJS.require, RequireJS.define));

