const mqtt = require('mqtt')
var database = require("./database.js")
const client = mqtt.connect('mqtt://localhost')

const PRESSURE_TOPIC = 'Ventilator/pressure'
const FLOWRATE_TOPIC = 'Ventilator/flow_rate'
const VOLUME_TOPIC = 'Ventilator/volume'
const CHART_DATA_TOPIC = 'Ventilator/chart_data'

var self = module.exports = {
  mqtt_sender: function(topic, message) {
    client.publish(topic, message)
    console.log("Sender called");
  },

  mqtt_receiver: function() {
    console.log("Receiver called");
    client.on('connect', () => {
      client.subscribe(PRESSURE_TOPIC)
      client.subscribe(FLOWRATE_TOPIC)
      client.subscribe(VOLUME_TOPIC)
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
//        case VOLUME_TOPIC:
//          console.log(topic + " : " + message)
////          return self.mqtt_volume(message)
        case CHART_DATA_TOPIC:
          console.log(topic + " : " + message)
          return self.mqtt_chartdata(message)
      }
      console.log('No handler for topic %s', topic)
    });
  },

  mqtt_pressure: function(message) {
    console.log("Pressure : " + message)
    database.set_pressure(Number((parseFloat(message)).toFixed(2)))
  },

  mqtt_flowrate: function(message) {
    console.log("Flowrate : " + message)
    database.set_flow_rate(Number((parseFloat(message)).toFixed(2)))
  },

  mqtt_volume: function(message) {
    console.log("Volume : " + message)
    database.set_volume(Number((parseFloat(message)).toFixed(2)))
  },

  mqtt_chartdata: function(message) {
    console.log("Chart data : " + message)
    json_data = JSON.parse(message)

    time = (new Date(json_data.time)).getTime()
    pressure = Number((json_data.pressure).toFixed(2))
    flow_rate = Number((json_data.flow_rate).toFixed(2))
    volume = Number((json_data.volume).toFixed(2))

    database.set_pressure([time, pressure])
    database.set_flow_rate([time, flow_rate])
    database.set_volume([time, volume])
  }

};
