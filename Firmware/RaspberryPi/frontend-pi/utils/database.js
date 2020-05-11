var pressure = new Array(60);
var flow_rate = new Array(60);

module.exports = {
  add_pressure: function(data){
    pressure.unshift(data)
    pressure.pop()
    return pressure
  },

  add_flow_rate: function(data){
    flow_rate.unshift(data)
    flow_rate.pop()
    return flow_rate
  },

  get_pressure: function(){
    return pressure
  },

  get_flow_rate: function(){
    return flow_rate
  }
}
