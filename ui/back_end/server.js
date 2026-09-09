const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Enable CORS for all incoming cross-origin requests
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// Middleware to parse incoming JSON data
app.use(express.json());

// Serve static frontend files from the front_end directory
app.use(express.static(path.join(__dirname, '../front_end')));

// Explicit route handler for root URL
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../front_end/index.html'));
});

// API endpoint to handle JSON saving
app.post('/api/save-requirements', (req, res) => {
  const jsonContent = JSON.stringify(req.body, null, 2);

  // Path 1: main/front_end/data/json/requirements.json
  const path1 = path.join(__dirname, '../../data/json/requirements.json');
  // Path 2: main/back_end/requirements.json
  //const path2 = path.join(__dirname, 'requirements.json');

  try {
    // Ensure the directory exists for path1
    fs.mkdirSync(path.dirname(path1), { recursive: true });

    // Write files to both locations
    fs.writeFileSync(path1, jsonContent);
    // fs.writeFileSync(path2, jsonContent);

    res.status(200).json({ status: 'success', message: 'Files saved successfully!' });
  } catch (err) {
    console.error('Error writing file:', err);
    res.status(500).json({ status: 'error', message: 'Failed to write file' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});