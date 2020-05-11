var pressure = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var flow_rate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

module.exports = {
  add_pressure: function(data){
    pressure.pop()
    pressure.unshift(data)
    console.log(pressure);
    return pressure
  },

  add_flow_rate: function(data){
    flow_rate.pop()
    flow_rate.unshift(data)
    console.log(flow_rate);
    return flow_rate
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
