const mqtt = require('mqtt')
var database = require("./database.js")
var dateFormat = require('dateformat');

const client = mqtt.connect('mqtt://localhost')

const CHART_DATA_TOPIC = 'Ventilator/chart_data'
const ACTUAL_TIDAL_VOLUME_TOPIC = 'Ventilator/vt'
const MINUTE_VOLUME_TOPIC = 'Ventilator/minute_volume'
const PIP_TOPIC = 'Ventilator/pip'
const ALARM_TOPIC = 'Ventilator/alarms'

var self = module.exports = {
  mqtt_sender: function(topic, message) {
    client.publish(topic, message)
    console.log("Sender called");
  },

  mqtt_receiver: function() {
    console.log("Receiver called");
    client.on('connect', () => {
      client.subscribe(CHART_DATA_TOPIC)
      client.subscribe(ACTUAL_TIDAL_VOLUME_TOPIC)
      client.subscribe(MINUTE_VOLUME_TOPIC)
      client.subscribe(PIP_TOPIC)
      client.subscribe(ALARM_TOPIC)
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
        case ALARM_TOPIC:
          return self.mqtt_alarms(message)
      }
      console.log('No handler for topic %s', topic)
    });
  },

  mqtt_alarms: function(message) {
    json_data = JSON.parse(message)

    timestamp = new Date(json_data.time)
    dateFormat(timestamp, "h:MM:ss TT");
    code = json_data.code
    active = json_data.active
    level = json_data.level
    message = "[ " + timestamp + " ] Code = " + code + " -- " + json_data.message

    if (active == true) {
      database.add_alarm(code, level, message)
    } else if (active == false) {
      database.remove_alarm(code, level)
    }
    console.log(message)
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
    database.set_vt(parseInt(message))
    console.log("MQTT VT: " + parseInt(message));
  },

  mqtt_minute_volume: function(message) {
    database.set_minute_volume(parseInt(message))
    console.log("MQTT Minute Volume: " + parseInt(message));
  },

  mqtt_pip: function(message) {
    database.set_pip((parseFloat(message)).toFixed(1))
    console.log("MQTT Pip: " + (parseInt(message)));
  }

};
