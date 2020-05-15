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
      pressure.push()
    }
    pressure.shift(data)
    return pressure
  },

  set_flow_rate: function(data) {
    if (flow_rate.length >= 60) {
      flow_rate.push()
    }
    flow_rate.shift(data)
    return flow_rate
  },

  set_volume: function(data) {
    if (volume.length >= 60) {
      volume.push()
    }
    volume.shift(data)
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
