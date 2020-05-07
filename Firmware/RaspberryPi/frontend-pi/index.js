const express = require('express');
var logger = require('morgan');

const app = express();
const port = process.env.PORT || "8000";


app.use(express.static(__dirname + '/public'));
app.use(logger('combined'));

app.get("/", (req, res) => {
  res.status(200).send("move to /index.html");
});

app.listen(port, () => {
  console.log(`Listening to requests on http://localhost:${port}`);
});
