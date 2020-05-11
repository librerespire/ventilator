const mqtt = require('mqtt')
var database = require("./database.js")
const client = mqtt.connect('mqtt://localhost')

var self = module.exports = {
  mqtt_sender: function() {
    console.log("Sender called");
  },

  mqtt_receiver: function() {
    console.log("Receiver called");
    client.on('connect', () => {
      client.subscribe('Ventilator/pressure')
      client.subscribe('Ventilator/flow_rate')
      client.subscribe('Ventilator/volume')
    });

    client.on('message', (topic, message) => {
      switch (topic) {
        case 'Ventilator/pressure':
          console.log(topic + " : " + message)
          return self.mqtt_pressure(message)
        case 'Ventilator/flow_rate':
          console.log(topic + " : " + message)
          return self.mqtt_flowrate(message)
        case 'Ventilator/volume':
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
