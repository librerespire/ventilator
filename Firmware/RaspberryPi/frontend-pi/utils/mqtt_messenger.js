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
    });

    client.on('message', (topic, message) => {
      switch (topic) {
        case 'Ventilator/pressure':
          console.log(topic + " : " + message)
          return self.mqtt_pressure(message)
        case 'Ventilator/flow_rate':
          console.log(topic + " : " + message)
          return self.mqtt_flowrate(message)
      }
      console.log('No handler for topic %s', topic)
    });
  },

  mqtt_pressure: function(message) {
    console.log(message)
    database.add_pressure(message)
    console.log(database.get_pressure())
  },

  mqtt_flowrate: function(message) {
    console.log(message)
    database.add_flow_rate(message)
    console.log(database.get_flow_rate())
  }

};
