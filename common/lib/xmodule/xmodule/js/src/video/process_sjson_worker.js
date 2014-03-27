var reply = function (data) {
    postMessage(data);
};

var invoke = function (list, method) {
    var index = 0,
        len = list.length,
        result = [];

    while (index < len) {
        list[index] = method(method, oldSpeed, newSpeed);
        index++;
    }

    return result;
};

var convertor = function (oldSpeed, newSpeed) {
    return function (value) {
        return value * newSpeed / oldSpeed;
    };
};

onmessage = function (data) {
    var sjson = data.sjson,
        oldSpeed = data.oldSpeed,
        newSpeed = data.newSpeed,
        processedData;

    processedData = {
        start: invoke(sjson.start, convertor(oldSpeed, newSpeed)),
        end: invoke(sjson.end, convertor(oldSpeed, newSpeed)),
        text: data.sjson.text
    };

    reply(processedData);
};


