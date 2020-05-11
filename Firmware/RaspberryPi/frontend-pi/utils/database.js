var p1 = [0,0];

module.exports = {
  add: function(p1_data){
    p1.unshift(p1_data)
    p1.pop()
    return p1
  }

}
