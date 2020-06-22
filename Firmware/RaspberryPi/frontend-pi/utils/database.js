var pressure = [];
var flow_rate = [];
var volume = [];
var tidle_volume
var minute_volume
var pip
var major_alarms = {}   // major alarms {'code':'message'}
var minor_alarms = {}   // minor alarms {'code':'message'}


module.exports = {

  add_alarm: function(code, level, message) {
    if (level == "MAJOR") {
      major_alarms[code] = message
      console.log("Added major alarm " + message)
    } else if (level == "MINOR") {
      minor_alarms[code] = message
      console.log("Added minor alarm " + message)
    }
  },

  remove_alarm: function(code, level) {
    if (level == "MAJOR") {
      delete major_alarms[code]
      console.log("Removed major alarm " + message)
    } else if (level == "MINOR") {
      console.log("Removed minor alarm " + message)
      delete minor_alarms[code]
    }
  },

  set_vt: function(data) {
    tidle_volume = data
  },

  set_minute_volume: function(data) {
    minute_volume = data
  },

  set_pip: function(data) {
    pip = data
  },

  set_pressure: function(data) {
    if (pressure.length >= 60) {
      pressure.shift()
    }
    pressure.push(data)
    return pressure
  },

  set_flow_rate: function(data) {
    if (flow_rate.length >= 60) {
      flow_rate.shift()
    }
    flow_rate.push(data)
    return flow_rate
  },

  set_volume: function(data) {
    if (volume.length >= 60) {
      volume.shift()
    }
    volume.push(data)
    return volume
  },

  get_vt: function() {
    return tidle_volume
  },

  get_minute_volume: function() {
    return minute_volume
  },

  get_pip: function() {
    return pip
  },

  get_volume: function() {
    return volume
  },

  get_pressure: function() {
    return pressure
  },

  get_flow_rate: function() {
    return flow_rate
  }
}
