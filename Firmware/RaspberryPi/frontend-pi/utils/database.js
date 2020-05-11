const sqlite3 = require('sqlite3')

var db;

module.exports = {
  create_db: function() {
    db = new sqlite3.Database(':memory:', (err) => {
      if (err) {
        return console.error(err.message);
      }
      console.log('Connected to the in-memory SQlite database.');
      db.run('CREATE TABLE p1(value real)'function(err) {
        if (err) {
          return console.log(err.message);
        }
        console.log('p1 table created');
      });

    });
  },


}
