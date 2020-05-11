const mqtt = require('mqtt')
var database = require("./database.js")
const client = mqtt.connect('mqtt://localhost')

module.exports = {
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
          return database.add_pressure(message)
        case 'Ventilator/flow_rate':
          return database.flow_rate(message)
      }
      console.log('No handler for topic %s', topic)
    });
  },

};
