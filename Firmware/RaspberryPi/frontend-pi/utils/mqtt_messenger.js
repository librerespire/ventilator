const mqtt = require('mqtt')
const client = mqtt.connect('mqtt://localhost:1883')

module.exports = {
  mqtt_sender: function() {
    console.log("Sender called");
  },

  mqtt_receiver: function() {
    console.log("Receiver called");
    client.on('connect', () => {
      client.subscribe('Ventilator/p1')
      client.subscribe('Ventilator/p2')
    });

    client.on('message', (topic, message) => {
      switch (topic) {
        case 'Ventilator/p1':
          return self.ven_p1(message)
        case 'Ventilator/p2':
          return self.ven_p2(message)
      }
      console.log('No handler for topic %s', topic)
    });
  },

  ven_p1: function(message){
    console.log(message);
  },

  ven_p2: function(message){
    console.log(message);
  }
};
