var pressure = [];
var flow_rate = [];
var volume = [];


module.exports = {
  set_time: function(data) {
    time.pop()
    time.unshift(data)
    return time
  },

  set_pressure: function(data) {
    if (pressure.length >= 60) {
      pressure.pop()
    }
    pressure.unshift(data)
    return pressure
  },

  set_flow_rate: function(data) {
    if (flow_rate.length >= 60) {
      flow_rate.pop()
    }
    flow_rate.unshift(data)
    return flow_rate
  },

  set_volume: function(data) {
    if (volume.length >= 60) {
      volume.pop()
    }
    volume.unshift(data)
    return volume
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
