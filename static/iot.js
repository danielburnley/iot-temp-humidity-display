var iotApp = angular.module('iotApp', []);
var temperature_graph_layout = {
    title: 'Temperature Over Time (Rolling Average)',
    xaxis: {
        title: "Time (GMT)"
    },
    yaxis: {
        title: "Temperature (&deg;C)",
        fixedrange: true
    }
};
var humidity_graph_layout = {
    title: 'Humidity Over Time (Rolling Average)',
    xaxis: {
        title: "Time (GMT)"
    },
    yaxis: {
        title: "Humidity (%)",
        fixedrange: true
    }
};

function create_graph(graph_div, data, graph_layout) {
    Plotly.newPlot(graph_div, [data], graph_layout, {displayModeBar: false});
}

function format_date(date) {
    var day = date.getDate().toString();
    var month = (date.getMonth() + 1).toString();
    var year = date.getFullYear().toString();
    var hour  = date.getHours().toString();
    var minute = date.getMinutes().toString();
    var second = date.getSeconds().toString();
    return day + "/" + month + "/" + year + " " + hour + ":" + minute + ":" + second;
}

iotApp.controller('HomeController', function HomeController($scope, $http) {
    $scope.raw_temperature = [];
    $scope.rolling_temperature = [];
    $scope.raw_humidity = [];
    $scope.rolling_humidity = [];
    $scope.overview = undefined;
    $scope.show_raw_data = false;
    $scope.raw_data = [];

    function get_overview() {
        return $http({
            method: 'GET',
            url: '/api/get/overview'
        }).then(function (response) {
            $scope.overview = response.data;
        });
    }

    function get_raw_temperature_readings() {
        return $http({
            method: 'GET',
            url: '/api/get/temp/hour/raw'
        }).then(function (response) {
            $scope.raw_temperature = response.data;
            combine_raw_data();
        });
    }

    function get_rolling_temperature_readings() {
        return $http({
            method: 'GET',
            url: '/api/get/temp/hour/rolling'
        }).then(function (response) {
            var data = {
                x: [],
                y: [],
                mode: 'lines'
            };
            for (var i = 0; i < response.data.length; i++) {
                var date = new Date(response.data[i].time * 1000);
                data.x.push(date);
                data.y.push(response.data[i].data);
            }
            create_graph('temperature-graph', data, temperature_graph_layout);
            $scope.rolling_temperature = response.data;
        });
    }

    function get_raw_humidity_readings() {
        return $http({
            method: 'GET',
            url: '/api/get/hum/hour/raw'
        }).then(function (response) {
            $scope.raw_humidity = response.data
            combine_raw_data();
        });
    }

    function get_rolling_humidity_readings() {
        return $http({
            method: 'GET',
            url: '/api/get/hum/hour/rolling'
        }).then(function (response) {
            var data = {
                x: [],
                y: [],
                mode: 'lines'
            };
            for (var i = 0; i < response.data.length; i++) {
                var date = new Date(response.data[i].time * 1000);
                data.x.push(date);
                data.y.push(response.data[i].data);
            }

            create_graph('humidity-graph', data, humidity_graph_layout);
            $scope.rolling_humidity = response.data;
        });
    }

    function combine_raw_data() {
        if ($scope.raw_humidity.length === 0 || $scope.raw_temperature.length === 0) {
            return;
        }
        var max_range = 0;
        if ($scope.raw_humidity.length > $scope.raw_temperature.length) {
            max_range = $scope.raw_humidity.length;
        } else {
            max_range = $scope.raw_temperature.length;
        }
        var data = [];
        for (var i = 0; i < max_range; i++) {
            data.push({
                "time": format_date(new Date($scope.raw_temperature[i].time * 1000)),
                "temp": $scope.raw_temperature[i].data,
                "hum": $scope.raw_humidity[i].data
            });
        }
        $scope.raw_data = data;
    }

    $scope.refresh_readings = function () {
        get_raw_temperature_readings();
        get_rolling_temperature_readings();
        get_raw_humidity_readings();
        get_rolling_humidity_readings();
        get_overview();
        setTimeout($scope.refresh_readings, 5000);
    };

    $scope.refresh_readings();

});