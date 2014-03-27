(function (requirejs, require, define) {

define(
'video/00_sjson.js',
['video/00_process.js'],
function(Process) {
"use strict";
/**
 * Provides convenient way to process big amount of data without UI blocking.
 *
 * @param {array} list Array to process.
 * @param {function} process Calls this function on each item in the list.
 * @return {array} Returns a Promise object to observe when all actions of a
                   certain type bound to the collection, queued or not, have finished.
 */

    var WorkerAdapter = function (worker) {
        this._worker = worker;
    };

    WorkerAdapter.prototype = {
        convert: function (sjson, oldSpeed, newSpeed) {
            var dfd = $.Deferred();

            this._worker.postMessage({
                sjson: sjson,
                oldSpeed: oldSpeed,
                newSpeed: newSpeed
            });

            this._worker.onmessage = dfd.resolve;
            this._worker.onerror = dfd.reject;

            return dfd.promise();
        }
    };

    var ProcessAdapter = function () {};

    ProcessAdapter.prototype = {
        process: function (oldSpeed, newSpeed) {
            return function (value) {
                return value * newSpeed / oldSpeed;
            };
        },
        convert: function (sjson, oldSpeed, newSpeed) {
            var dfd = $.Deferred();

            $.when(
                Process.array(sjson.start, this.process(oldSpeed, newSpeed)),
                Process.array(sjson.end, this.process(oldSpeed, newSpeed))
            ).done(function (start, end) {
                dfd.resolve({
                    start: start,
                    end: end,
                    text: sjson.text
                });
            })
            .fail(dfd.reject);

            return dfd.promise();
        }
    };


    var Sjson = (function () {
        var cache = {},
            worker,
            hasWorker = (function () {
                var noWorker = _.isUndefined(window.Worker);

                if(!noWorker) {
                    try {
                        worker = new Worker("process_sjson_worker.js");
                    } catch (ex) {
                        noWorker = true;
                    }
                }

                return noWorker;
            }());

        var convert = (function () {
            var converter = hasWorker ?
                new WorkerAdapter(worker):
                new ProcessAdapter();

            return function (sjson, oldSpeed, newSpeed) {
                return converter.convert(sjson, oldSpeed, newSpeed);
            };
        }());

        return {
            convert: convert
        };
    }());

    return Sjson;
});
}(RequireJS.requirejs, RequireJS.require, RequireJS.define));

