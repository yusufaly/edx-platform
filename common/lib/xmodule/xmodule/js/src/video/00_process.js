(function (requirejs, require, define) {

define(
'video/00_process.js',
[],
function() {
    "use strict";
/**
 * Provides convenient way to process big amount of data without UI blocking.
 *
 * @param {array} list Array to process.
 * @param {function} process Calls this function on each item in the list.
 * @return {array} Returns a Promise object to observe when all actions of a
                   certain type bound to the collection, queued or not, have finished.
 */
    var Process = {
        array: function (list, process) {
            var MAX_DELAY = 50, // maximum amount of time that js code should be allowed to run continuously
                dfd = $.Deferred(),
                result = [],
                index = 0,
                len;

            if (!_.isArray(list)) {
                return dfd.reject().promise();
            } else if (!_.isFunction(process) || !list.length) {
                return dfd.resolve(list).promise();
            } else {
                len = list.length;
            }

            var getCurrentTime = function () {
                return (new Date()).getTime();
            };

            var handler = function () {
                var start = getCurrentTime();

                do {
                    result[index] = process(list[index]);
                    index++;
                } while (index < len && getCurrentTime() - start < MAX_DELAY);

                if (index < len) {
                    setTimeout(handler, 25);
                } else {
                    dfd.resolve(result);
                }
            };

            setTimeout(handler, 25);

            return dfd.promise();
        }
    };

    return Process;
});
}(RequireJS.requirejs, RequireJS.require, RequireJS.define));

