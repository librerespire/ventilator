const mqtt = require('mqtt')
var database = require("./database.js")
const client = mqtt.connect('mqtt://localhost')

const PRESSURE_TOPIC = 'Ventilator/pressure'
const FLOWRATE_TOPIC = 'Ventilator/flow_rate'
const VOLUME_TOPIC = 'Ventilator/volume'
const CHART_DATA_TOPIC = 'Ventilator/chart_data'
const ACTUAL_TIDAL_VOLUME_TOPIC = 'Ventilator/vt'

var self = module.exports = {
  mqtt_sender: function(topic, message) {
    client.publish(topic, message)
    console.log("Sender called");
  },

  mqtt_receiver: function() {
    console.log("Receiver called");
    client.on('connect', () => {
      client.subscribe(ACTUAL_TIDAL_VOLUME_TOPIC)
      client.subscribe(CHART_DATA_TOPIC)
    });

    client.on('message', (topic, message) => {
      switch (topic) {
//        case PRESSURE_TOPIC:
//          console.log(topic + " : " + message)
////          return self.mqtt_pressure(message)
//        case FLOWRATE_TOPIC:
//          console.log(topic + " : " + message)
////          return self.mqtt_flowrate(message)
       case ACTUAL_TIDAL_VOLUME_TOPIC:
         console.log(topic + " : " + message)
          return self.mqtt_vt(message)
        case CHART_DATA_TOPIC:
          return self.mqtt_chartdata(message)
      }
      console.log('No handler for topic %s', topic)
    });
  },

  mqtt_pressure: function(message) {
    database.set_pressure(Number((parseFloat(message)).toFixed(2)))
  },

  mqtt_flowrate: function(message) {
    database.set_flow_rate(Number((parseFloat(message)).toFixed(2)))
  },

  mqtt_volume: function(message) {
    database.set_volume(Number((parseFloat(message)).toFixed(2)))
  },

  mqtt_vt: function(message) {
    database.set_vt(Number((parseFloat(message)).toFixed(2)))
  },

  mqtt_chartdata: function(message) {
    json_data = JSON.parse(message)

    time = new Date(json_data.time)
    pressure = Number((json_data.pressure).toFixed(2))
    flow_rate = Number((json_data.flow_rate).toFixed(2))
    volume = Number((json_data.volume).toFixed(2))

    database.set_pressure([time, pressure])
    database.set_flow_rate([time, flow_rate])
    database.set_volume([time, volume])
  }

};
