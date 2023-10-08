const express = require("express");
const app = express();
const fs = require('fs');

app.listen(3000, () => {
  console.log("Application started and Listening on port 3000");
});

app.set('view engine', 'ejs')

app.use(express.static(__dirname));
console.log(__dirname)

let results = fs.readFileSync('../database/results.json');
results = JSON.parse(results);

app.get("/", (req, res) => {
  res.render("index", {results:results});
});

