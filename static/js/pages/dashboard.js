/**
 * Theme: Greeva - Responsive Bootstrap 5 Admin Dashboard
 * Author: Coderthemes
 * Module/App: Dashboard
 */



//
// Daily Sales CHART
//

var colors = ["#6b5eae", "#31ce77", "#fa5c7c", "#fbcc5c"];
var dataColors = $("#daily-sales").data('colors');
if (dataColors) {
    colors = dataColors.split(",");
}

var options = {
    series: [
        {
            name: "Orders",
            type: "line",
            data: [
                89.25, 98.58, 68.74, 108.87, 77.54, 84.03, 51.24, 28.57, 92.57, 42.36, 88.51, 36.57,
            ],
        }, {
            name: "Delivered",
            type: "line",
            data: [
                22.25, 24.58, 36.74, 22.87, 19.54, 25.03, 29.24, 10.57, 24.57, 35.36, 20.51, 17.57,
            ],
        }
    ],
    chart: {
        height: 300,
        type: "line",
        toolbar: {
            show: false,
        },
    },
    stroke: {
        dashArray: [0, 5],
        width: [2, 2],
        curve: 'smooth'
    },
    fill: {
        opacity: [1, 1],
        type: ['gradient', 'gradient'],
        gradient: {
            shade: 'dark',
            gradientToColors: ['#FDD835'],
            type: "horizontal",
            shadeIntensity: 1,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100, 100, 100]
        },
    },
    markers: {
        size: [0, 0, 0, 0],
        strokeWidth: 2,
        hover: {
            size: 4,
        },
    },
    xaxis: {
        categories: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        axisTicks: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    yaxis: {
        stepSize: 25,
        min: 0,
        labels: {
            formatter: function (val) {
                return val + "k";
            },
            offsetX: -15
        },
        axisBorder: {
            show: false,
        }
    },
    grid: {
        show: true,
        xaxis: {
            lines: {
                show: false,
            },
        },
        yaxis: {
            lines: {
                show: true,
            },
        },
        padding: {
            top: 0,
            right: -15,
            bottom: 15,
            left: -15,
        },
    },
    legend: {
        show: true,
        horizontalAlign: "center",
        offsetX: 0,
        offsetY: -5,
        markers: {
            width: 9,
            height: 9,
            radius: 6,
        },
        itemMargin: {
            horizontal: 10,
            vertical: 0,
        },
    },
    plotOptions: {
        bar: {
            columnWidth: "50%",
            barHeight: "70%",
            borderRadius: 3,
        },
    },
    colors: colors,
    tooltip: {
        shared: true,
        y: [{
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        },
        {
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        }
        ],
    },
}

var chart = new ApexCharts(
    document.querySelector("#daily-sales"),
    options
);

chart.render();

//
// Statistics CHART
//
///
var colors = ["#6b5eae", "#31ce77", "#fa5c7c", "#fbcc5c"];
var dataColors = $("#statistics-chart").data('colors');
if (dataColors) {
    colors = dataColors.split(",");
}

var options = {
    series: [
        {
            name: "Open Compaign",
            type: "bar",
            data: [
                89.25, 98.58, 68.74, 108.87, 77.54, 84.03, 51.24, 28.57, 92.57, 42.36, 88.51, 36.57,
            ],
        }, {
            name: "Marketing Cost",
            type: "bar",
            data: [
                30.28, 33.45, 50.0, 31.12, 26.59, 34.06, 39.79, 14.38, 33.44, 48.12, 27.91, 23.91
            ],
        }
    ],
    chart: {
        height: 301,
        type: "line",
        toolbar: {
            show: false,
        },
    },
    stroke: {
        dashArray: [0, 0, 0, 8],
        width: [0, 0, 2, 2],
        curve: 'smooth'
    },
    fill: {
        opacity: [1, 1],
        type: ['gradient', 'gradient'],
        gradient: {
            shade: 'dark',
            gradientToColors: ['#35b8e0'],
            type: "vertical",
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100]
        },
    },
    markers: {
        size: [0, 0, 0, 0],
        strokeWidth: 2,
        hover: {
            size: 4,
        },
    },
    xaxis: {
        categories: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        axisTicks: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    yaxis: {
        stepSize: 25,
        min: 0,
        labels: {
            formatter: function (val) {
                return val + "k";
            },
            offsetX: -15
        },
        axisBorder: {
            show: false,
        }
    },
    grid: {
        show: true,
        xaxis: {
            lines: {
                show: false,
            },
        },
        yaxis: {
            lines: {
                show: true,
            },
        },
        padding: {
            top: 0,
            right: -15,
            bottom: 15,
            left: -15,
        },
    },
    legend: {
        show: true,
        horizontalAlign: "center",
        offsetX: 0,
        offsetY: -5,
        markers: {
            width: 9,
            height: 9,
            radius: 6,
        },
        itemMargin: {
            horizontal: 10,
            vertical: 0,
        },
    },
    plotOptions: {
        bar: {
            columnWidth: "50%",
            barHeight: "70%",
            borderRadius: 3,
        },
    },
    colors: colors,
    tooltip: {
        shared: true,
        y: [{
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        },
        {
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        },
        {
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        },
        {
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        },
        ],
    },
}

var chart = new ApexCharts(
    document.querySelector("#statistics-chart"),
    options
);

chart.render();

//
// REVENUE AREA CHART
//
///
var colors = ["#6b5eae", "#31ce77", "#fa5c7c", "#fbcc5c"];
var dataColors = $("#revenue-chart").data('colors');
if (dataColors) {
    colors = dataColors.split(",");
}

var options = {
    series: [
        {
            name: "Total Income",
            type: "area",
            data: [
                81.98, 90.55, 63.14, 100.0, 71.22, 77.18, 47.07, 26.24, 85.03, 38.91, 81.3, 33.59
            ],
        }, {
            name: "Total Expenses",
            type: "area",
            data: [
                30.28, 33.45, 50.0, 31.12, 26.59, 34.06, 39.79, 14.38, 33.44, 48.12, 27.91, 23.91
            ],
        }
    ],
    chart: {
        height: 300,
        type: "line",
        toolbar: {
            show: false,
        },
    },
    stroke: {
        dashArray: [0, 0, 0, 8],
        width: [0, 0, 2, 2],
        curve: 'smooth'
    },
    fill: {
        opacity: [1, 1],
        type: ['gradient', 'gradient'],
        gradient: {
            shade: 'dark',
            gradientToColors: ['#35b8e0'],
            type: "vertical",
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.7,
            stops: [0, 100]
        },
    },
    markers: {
        size: [0, 0, 0, 0],
        strokeWidth: 2,
        hover: {
            size: 4,
        },
    },
    xaxis: {
        categories: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        axisTicks: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    yaxis: {
        stepSize: 25,
        min: 0,
        labels: {
            formatter: function (val) {
                return val + "k";
            },
            offsetX: -10
        },
        axisBorder: {
            show: false,
        }
    },
    grid: {
        show: true,
        xaxis: {
            lines: {
                show: false,
            },
        },
        yaxis: {
            lines: {
                show: true,
            },
        },
        padding: {
            top: 0,
            right: 0,
            bottom: 15,
            left: 0,
        },
    },
    legend: {
        show: true,
        horizontalAlign: "center",
        offsetX: 0,
        offsetY: -5,
        markers: {
            width: 9,
            height: 9,
            radius: 6,
        },
        itemMargin: {
            horizontal: 10,
            vertical: 0,
        },
    },
    plotOptions: {
        bar: {
            columnWidth: "50%",
            barHeight: "70%",
            borderRadius: 3,
        },
    },
    colors: colors,
    tooltip: {
        shared: true,
        y: [{
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        },
        {
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return "$" + y.toFixed(2) + "k";
                }
                return y;
            },
        }
        ],
    },
}

var chart = new ApexCharts(
    document.querySelector("#revenue-chart"),
    options
);

chart.render();

//
// data-visits- CHART
//
var colors = ["#6b5eae", "#35b8e0", "#31ce77", "#fa5c7c", "#e3eaef"];
var dataColors = $("#data-visits-chart").data('colors');
if (dataColors) {
    colors = dataColors.split(",");
}

var options = {
    chart: {
        height: 347,
        type: 'donut',
    },
    series: [25, 40, 30, 15, 20], // Example age group data
    legend: {
        show: true,
        position: 'bottom',
        horizontalAlign: 'center',
        verticalAlign: 'middle',
        floating: false,
        fontSize: '14px',
        offsetX: 0,
        offsetY: 7
    },
    labels: ["10-16 (Child)", "18-26 (Young)", "27-35 (Adult)", "36-50 (Middle Age)", "51+ (Senior)"], // Age groups
    colors: colors,
    responsive: [{
        breakpoint: 600,
        options: {
            chart: {
                height: 240
            },
            legend: {
                show: false
            },
        }
    }],
    fill: {
        type: ['gradient'],
        gradient: {
            shade: 'dark',
            gradientToColors: ['#35b8e0'],
            type: "vertical",
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.7,
            stops: [0, 100]
        },
    }
};

var chart = new ApexCharts(
    document.querySelector("#data-visits-chart"),
    options
);

chart.render();


class VectorMap {

    // World Map Markers with Line
    initWorldMarkerLine() {
        const worldlinemap = new jsVectorMap({
            map: "world_merc",
            selector: "#world-map-markers-line",
            zoomOnScroll: false,
            zoomButtons: false,
            markers: [{
                name: "Greenland",
                coords: [72, -42]
            },
            {
                name: "Canada",
                coords: [56.1304, -106.3468]
            },
            {
                name: "Brazil",
                coords: [-14.2350, -51.9253]
            },
            {
                name: "Egypt",
                coords: [26.8206, 30.8025]
            },
            {
                name: "Russia",
                coords: [61, 105]
            },
            {
                name: "China",
                coords: [35.8617, 104.1954]
            },
            {
                name: "United States",
                coords: [37.0902, -95.7129]
            },
            {
                name: "Norway",
                coords: [60.472024, 8.468946]
            },
            {
                name: "Ukraine",
                coords: [48.379433, 31.16558]
            },
            ],
            lines: [{
                from: "Canada",
                to: "Egypt"
            },
            {
                from: "Russia",
                to: "Egypt"
            },
            {
                from: "Greenland",
                to: "Egypt"
            },
            {
                from: "Brazil",
                to: "Egypt"
            },
            {
                from: "United States",
                to: "Egypt"
            },
            {
                from: "China",
                to: "Egypt"
            },
            {
                from: "Norway",
                to: "Egypt"
            },
            {
                from: "Ukraine",
                to: "Egypt"
            },
            ],
            regionStyle: {
                initial: {
                    stroke: "#9ca3af",
                    strokeWidth: 0.25,
                    fill: '#9ca3af69',
                    fillOpacity: 1,
                },
            },
            markerStyle: {
                initial: { fill: "#9ca3af" },
                selected: { fill: "#9ca3af" }
            },
            lineStyle: {
                animation: true,
                strokeDasharray: "6 3 6",
            },
        });
    }

    init() {
        this.initWorldMarkerLine();
    }

}

document.addEventListener('DOMContentLoaded', function (e) {
    new VectorMap().init();
});