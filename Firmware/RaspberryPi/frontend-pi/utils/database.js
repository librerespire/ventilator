var pressure = [];
var flow_rate = [];
var volume = [];
var tidle_volume


module.exports = {
  set_vt: function(data) {
    tidle_volume = data
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

  get_volume: function() {
    return volume
  },

  get_vt: function() {
    return tidle_volume
  },

  get_pressure: function() {
    return pressure
  },

  get_flow_rate: function() {
    return flow_rate
  }
}
