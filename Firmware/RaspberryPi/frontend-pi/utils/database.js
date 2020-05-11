var p1 = [];

module.exports = {
  update_p1: function(p1_data){
    p1.unshift(p1_data)
    p1.pop()
    return p1
  }

}
