const mqtt = require('mqtt')
var database = require("./database.js")
const client = mqtt.connect('mqtt://localhost')

const CHART_DATA_TOPIC = 'Ventilator/chart_data'
const ACTUAL_TIDAL_VOLUME_TOPIC = 'Ventilator/vt'
const MINUTE_VOLUME_TOPIC = 'Ventilator/minute_volume'
const PIP_TOPIC = 'Ventilator/pip'

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
      console.log(topic + " : " + message)
      switch (topic) {
        case CHART_DATA_TOPIC:
          return self.mqtt_chartdata(message)
        case ACTUAL_TIDAL_VOLUME_TOPIC:
          return self.mqtt_vt(message)
        case MINUTE_VOLUME_TOPIC:
          return self.mqtt_minute_volume(message)
        case PIP_TOPIC:
          return self.mqtt_pip(message)
      }
      console.log('No handler for topic %s', topic)
    });
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
  },

  mqtt_vt: function(message) {
    database.set_vt((parseFloat(message)).toFixed(2))
    console.log("MQTT VT: " + (parseFloat(message)).toFixed(2));
  },

  mqtt_minute_volume: function(message) {
    database.set_minute_volume((parseFloat(message)).toFixed(2))
    console.log("MQTT Minute Volume: " + (parseFloat(message)).toFixed(2));
  },

  mqtt_pip: function(message) {
    database.set_pip((parseFloat(message)).toFixed(2))
    console.log("MQTT Pip: " + (parseFloat(message)).toFixed(2));
  }

};
