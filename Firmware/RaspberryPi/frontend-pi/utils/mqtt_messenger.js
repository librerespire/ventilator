const mqtt = require('mqtt')
var database = require("./database.js")
const client = mqtt.connect('mqtt://localhost')

const PRESSURE_TOPIC = 'Ventilator/pressure'
const FLOWRATE_TOPIC = 'Ventilator/flow_rate'
const VOLUME_TOPIC = 'Ventilator/volume'

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
    });

    client.on('message', (topic, message) => {
      switch (topic) {
        case PRESSURE_TOPIC:
          console.log(topic + " : " + message)
          return self.mqtt_pressure(message)
        case FLOWRATE_TOPIC:
          console.log(topic + " : " + message)
          return self.mqtt_flowrate(message)
        case VOLUME_TOPIC:
          console.log(topic + " : " + message)
          return self.mqtt_volume(message)
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
  }

};
