const express = require('express');
const path = require('path');
const app = express();

// Define the directory where your static files are located
const publicDir = path.join(__dirname);

// Serve static files (like CSS or other JS files if you add them later)
app.use(express.static(publicDir));

// Specifically handle the request for the root URL ("/")
app.get('/', (req, res) => {
  res.sendFile(path.join(publicDir, 'frontend.html'));
});

// Start the server
const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});