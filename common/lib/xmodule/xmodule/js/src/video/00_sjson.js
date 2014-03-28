(function (requirejs, require, define) {

define(
'video/00_sjson.js',
[],
function(Process) {
"use strict";

    var Sjson = function (data) {
        var sjson = {
                start: data.start.concat(),
                text: data.text.concat()
            },
            module = {};

        var getter = function (propertyName) {
            return function () {
                return sjson[propertyName];
            };
        };

        return {
            getCaptions: getter('text'),
            getStartTimes: getter('start'),
            getSize: function () {
                return sjson.text.length;
            }
        };
    };

    return Sjson;
});
}(RequireJS.requirejs, RequireJS.require, RequireJS.define));

