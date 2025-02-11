const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const sqlite3 = require('sqlite3').verbose();
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server })

// Enable CORS for all routes
app.use(cors({
    origin: 'http://localhost:5173',  // Allow requests from your React app
    methods: ['GET', 'POST'],
    credentials: true
  }));

const db = new sqlite3.Database('../mosquito_detection.db', (err) => {
    if (err) {
        console.error('Error opening database', err);
    } else {
        console.log('Connected to SQLite database');
    }
});


const query = `
    SELECT
        m.name AS mosquito_name,
        m.description AS mosquito_description,
        GROUP_CONCAT(DISTINCT d.name) AS diseases,
        COUNT(DISTINCT md.id) AS detected_count, 
        ROUND(
        COUNT(DISTINCT md.id) * 100.0 / 
        (SELECT COUNT(DISTINCT id) FROM mosquito_detected),
        2
    ) AS detected_percentage
    FROM
        mosquito m
    LEFT JOIN
        mosquito_disease mdise ON m.id = mdise.mosquito_id
    LEFT JOIN
        disease d ON mdise.disease_id = d.id
    INNER JOIN
        mosquito_detected md ON m.name = md.species_name
    GROUP BY
        m.id;
`;

// WebSocket connection
wss.on('connection', (ws) => {
    console.log('New client connected');
  
    // Send initial data to the client
    db.all(query, (err, rows) => {
      if (err) {
        console.error('Error fetching data:', err);
        return;
      }
      ws.send(JSON.stringify(rows));
    });
  
    // Listen for database changes (e.g., using triggers or polling)
    // For simplicity, we'll use polling here
    const interval = setInterval(() => {
      db.all(query, (err, rows) => {
        if (err) {
          console.error('Error fetching data:', err);
          return;
        }
        ws.send(JSON.stringify(rows));
      });
    }, 5000); // Poll every 5 seconds
  
    // Handle client disconnect
    ws.on('close', () => {
      console.log('Client disconnected');
      clearInterval(interval);
    });
  });

// let lastDetectedCount = 0;

const getMosquitoStats = (callback) => {
    db.all(query, (err, rows) => {
        if (err) {
            console.error('Error fetching mosquito stats:', err);
            callback(null);
        } else {
            callback({ rows });
        }
    });
};


// Periodically check for changes in the database
// setInterval(() => {
//     getMosquitoStats((data) => {
//         if (data && data.total !== lastDetectedCount) {
//             lastDetectedCount = data.total;
//             io.emit('updateDetectedStats', data);
//         }
//     });
// }, 1000);

// Serve frontend
app.use(express.static('public'));

// API to get the current stats (initial load)
app.get('/api/detected-stats', (req, res) => {
    getMosquitoStats((data) => {
        if (data) {
            res.json(data);
        } else {
            res.status(500).json({ error: 'Unable to fetch mosquito stats' });
        }
    });
});

server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
