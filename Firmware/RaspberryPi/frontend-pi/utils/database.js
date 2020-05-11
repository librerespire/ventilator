var pressure = new Array(60).fill(0);
var flow_rate = new Array(60).fill(0);
var volume = new Array(60).fill(0);

module.exports = {
  set_pressure: function(data){
    pressure.pop()
    pressure.unshift(data)
    console.log(pressure);
    return pressure
  },

  set_flow_rate: function(data){
    flow_rate.pop()
    flow_rate.unshift(data)
    console.log(flow_rate);
    return flow_rate
  },

  set_volume: function(data){
    volume.pop()
    volume.unshift(data)
    console.log(volume);
    return volume
  },

  get_volume: function(){
    console.log(volume);
    return volume
  },

  get_pressure: function(){
    console.log(pressure);
    return pressure
  },

  get_flow_rate: function(){
    console.log(flow_rate);
    return flow_rate
  }
}
