var p1 = [0,0];
var p2 = [1,1];

module.exports = {
  add_p1: function(p1_data){
    p1.unshift(p1_data)
    p1.pop()
    return p1
  },

  add_p2: function(p2_data){
    p2.unshift(p2_data)
    p2.pop()
    return p2
  },

  get_p1: function(){
    return p1
  },

  get_p2: function(){
    return p1
  }
}
