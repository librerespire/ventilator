var pressure = new Array(60).fill(0);
var flow_rate = new Array(60).fill(0);

module.exports = {
  add_pressure: function(data){
    pressure.unshift(data)
    pressure.pop()
    console.log(pressure);
    return pressure
  },

  add_flow_rate: function(data){
    flow_rate.unshift(data)
    flow_rate.pop()
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
