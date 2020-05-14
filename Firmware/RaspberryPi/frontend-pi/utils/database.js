var pressure = new Array(60).fill(0);
var flow_rate = new Array(60).fill(0);
var volume = new Array(60).fill(0);
var time = new Array(60).fill(10);

var pressure_2d = new Array(60).fill(0).map(() => new Array(2).fill(0))

module.exports = {
  set_time: function(data){
    time.pop()
    time.unshift(data)
    return time
  },

  set_pressure: function(data){
    pressure.pop()
    pressure.unshift(data)
    return pressure
  },

  set_pressure_2d: function(data){
    pressure_data.pop()
    pressure_data.unshift(data)
    return pressure_2d
  },

  set_flow_rate: function(data){
    flow_rate.pop()
    flow_rate.unshift(data)
    return flow_rate
  },

  set_volume: function(data){
    volume.pop()
    volume.unshift(data)
    return volume
  },

  get_volume: function(){
    return volume
  },

  get_pressure: function(){
    return pressure
  },

  get_flow_rate: function(){
    return flow_rate
  },

  get_time: function(){
    return time
  }
}
