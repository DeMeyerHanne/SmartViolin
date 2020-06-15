// "use strict";

let html_addButton;
let currentTemp = 0;

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);


const listenToUI = function() {
    console.log("ListenToUI werkt");
    const knoppen = document.querySelectorAll(".js-koffer-btn");
    for (const knop of knoppen) {
        knop.addEventListener("click", function() {
            // const code = this.codeS;
            // const waarde = this.gemetenWaarde;
            console.log("Koffer kan geopend worden")
            socket.send("F2B_koffer_open");
        })
    };
};


//#region *** callback-visualitation - show__ ***
const showDataTemp = function(data) {
    console.log("Data temperatuur ingeladen")

    let converted_labels = [];
    let converted_data = [];
    for (const temp of data) {
        converted_labels.push(temp.eindDatum);
        converted_data.push(temp.gemetenWaarde);
    }
    console.log(converted_data)
    drawChartTemp(converted_labels, converted_data);
};

const showDataLucht = function(data) {
    console.log("Luchtvochtigheid is ingeladen")

    let converted_labels_lucht = [];
    let converted_data_lucht = [];
    for (const lucht of data) {
        converted_labels_lucht.push(lucht.eindDatum);
        converted_data_lucht.push(lucht.gemetenWaarde);
    }
    console.log(converted_data_lucht);
    drawChartLucht(converted_labels_lucht, converted_data_lucht);
};

const showDataOef = function(data) {
    console.log("oefentijd wordt getoond");

    let converted_labels_oef = [];
    let converted_data_oef = [];
    for (const oef of data) {
        converted_labels_oef.push(oef.eindDatum);
        converted_data_oef.push(oef.gemetenWaarde);
    }
    console.log(converted_data_oef);
    drawchartOef(converted_labels_oef, converted_data_oef);
};
//#endregion 

//#region *** draw-chart oef ***
const drawChartTemp = function(labels, data) {
    let ctx = document.querySelector('.js-chart-temp').getContext('2d');

    let config = {
        type: 'line', //specifiek welk type chart het is
        data: {
            labels: labels, // alle labels dat getoond worden op de x-as vd chart
            datasets: [
                {
                    label: 'Temperatuur',             // label die we bovenaan toevoegen
                    backgroundColor: 'white',    // styling
                    borderColor: 'black',          // styling
                    data: data,                  // de data die je wilt zetten op de chart
                    fill: false                  // styling
                }
            ]
        },
        options: { // options om de stijl en het gedrag van de chart te veranderen
            responsive: true,
            title: {
                display: true,
                // text: 'Chart.js Line Chart'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'EindDatum'
                        }
                    }
                ],
                yAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Meting'
                        }
                    }
                ]
            }
        }
    };

    let myChartTemp = new Chart(ctx, config);
};

const drawChartLucht = function(labels, data) {
    let ctx = document.querySelector('.js-chart-lucht').getContext('2d');

    let config = {
        type: 'line', //specifiek welk type chart het is
        data: {
            labels: labels, // alle labels dat getoond worden op de x-as vd chart
            datasets: [
                {
                    label: 'Luchtvochtigheid',   // label die we bovenaan toevoegen
                    backgroundColor: 'white',    // styling
                    borderColor: 'black',        // styling
                    data: data,                  // de data die je wilt zetten op de chart
                    fill: false                  // styling
                }
            ]
        },
        options: { // options om de stijl en het gedrag van de chart te veranderen
            responsive: true,
            title: {
                display: true,
                // text: 'Chart.js Line Chart'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'EindDatum'
                        }
                    }
                ],
                yAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Meting'
                        }
                    }
                ]
            }
        }
    };

    let myChartLucht = new Chart(ctx, config);
};

const drawchartOef = function(labels, data) {
    let ctx = document.querySelector('.js-chart-oef').getContext('2d');

    let config = {
        type: 'line', //specifiek welk type chart het is
        data: {
            labels: labels, // alle labels dat getoond worden op de x-as vd chart
            datasets: [
                {
                    label: 'Oefentijd',             // label die we bovenaan toevoegen
                    backgroundColor: 'white',    // styling
                    borderColor: 'black',          // styling
                    data: data,                  // de data die je wilt zetten op de chart
                    fill: false                  // styling
                }
            ]
        },
        options: { // options om de stijl en het gedrag van de chart te veranderen
            responsive: true,
            title: {
                display: true,
                text: 'Chart.js Line Chart'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'EindDatum'
                        }
                    }
                ],
                yAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Meting'
                        }
                    }
                ]
            }
        }
    };

    let myChartOef = new Chart(ctx, config);
};
//#endregion

//#region *** data access - get__ ***
const getLuchtData = function() {
    handleData(`http://${lanIP}/api/v1/waarden/1`, showDataLucht);
};
const getTempData = function() {
    handleData(`http://${lanIP}/api/v1/waarden/2`, showDataTemp);
};
const getOefData = function() {
    handleData(`http://${lanIP}/api/v1/waarden/3`, showDataOef);
};
//#endregion


//#region listenToSocket
const listenToSocket = function() {
    socket.on("connected", function() {
        console.log("verbonden met socket webserver");
        handleData(`http://${lanIP}/api/v1/x`, callbackWaardeTemp);
        handleData(`http://${lanIP}/api/v1/oefentijd`, callbackWaardeOefentijd);
        handleData(`http://${lanIP}/api/v1/luchtvochtigheid`, callbackWaardeLucht);
    });

    socket.on("B2F_verandering_koffer", function() {
        console.log("GELUKT");
    })
};
//#endregion


//#region callback
const callbackWaardeTemp = function(data) {
    console.log(data);
    // queryselector ophalen html met placeholder
    document.querySelector(".js-waarde").innerHTML = data.gemetenWaarde;
};
const callbackWaardeOefentijd = function(dataOef) {
    console.log(dataOef);
    document.querySelector(".js-oefentijd").innerHTML = dataOef.oefentijd;
};
const callbackWaardeLucht = function(dataLucht) {
    console.log(dataLucht);
    document.querySelector(".js-luchtvochtigheid").innerHTML = dataLucht.gemetenWaarde;
};
//#endregion    


// DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM geladen");
    listenToUI();
    listenToSocket();
    getOefData();
    getTempData();
    getLuchtData();
});