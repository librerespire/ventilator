var pressure = new Array(60).fill(0);
var flow_rate = new Array(60).fill(0);
var volume = new Array(60).fill(0);

module.exports = {
  set_pressure: function(data){
    pressure.pop()
    pressure.unshift(data)
    return pressure
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
  }
}
