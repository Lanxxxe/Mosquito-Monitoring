require('dotenv').config();

const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const mongoose = require('mongoose');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(cors({
    origin: 'http://localhost:5173',
    methods: ['GET', 'POST'],
    credentials: true
}));

// Connect to MongoDB
const mongoURI = process.env.MONGO_URI

mongoose.connect(mongoURI)
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('MongoDB connection error:', err));

// Define Mongoose models
const Mosquito = mongoose.model('mosquito', new mongoose.Schema({
    name: String,
    description: String,
    diseases: [mongoose.Schema.Types.ObjectId],
    image_path: String
}, { collection: 'mosquito' }));

const Disease = mongoose.model('disease', new mongoose.Schema({
    name: String
}, { collection: 'disease' }));

const MosquitoDetection = mongoose.model('mosquito_detected', new mongoose.Schema({
    species_name: String,
    detection_time: Date
}, { collection: 'mosquito_detected' }));

// Function to fetch mosquito statistics
const getMosquitoStats = async () => {
    try {
        // const totalDetections = await MosquitoDetection.countDocuments();
        // const mosData = await MosquitoDetection.find();
        // console.log(mosData);
        // const mos = await Mosquito.find();
        // console.log(mos);
        // const des = await Disease.find();
        // console.log(des);

        // Step 1: Count total detections
        const totalDetections = await MosquitoDetection.countDocuments();

        // Step 2: Aggregate mosquito detection counts
        const detectionCounts = await MosquitoDetection.aggregate([
            {
                $group: {
                    _id: "$species_name",
                    detected_count: { $sum: 1 }
                }
            }
        ]);

        // Step 3: Fetch all mosquito details
        const mosquitoes = await Mosquito.find();

        // Step 4: Fetch disease details
        const diseases = await Disease.find();

        // Step 5: Map mosquito data
        const mosquitoStats = detectionCounts.map(detection => {
            // Find matching mosquito details
            const mosquitoInfo = mosquitoes.find(m => m.name === detection._id);
            
            if (!mosquitoInfo) return null;

            // Find diseases associated with the mosquito
            const diseaseNames = mosquitoInfo.diseases.map(diseaseId => {
                const disease = diseases.find(d => d._id.equals(diseaseId));
                return disease ? disease.name : null;
            }).filter(Boolean).join(', ');

            // Compute detection percentage
            const detected_percentage = ((detection.detected_count / totalDetections) * 100).toFixed(2);

            return {
                mosquito_name: mosquitoInfo.name,
                mosquito_description: mosquitoInfo.description,
                diseases: diseaseNames,
                detected_count: detection.detected_count,
                detected_percentage: parseFloat(detected_percentage)
            };
        }).filter(Boolean);

        return { rows: mosquitoStats };
    } catch (err) {
        console.error('Error fetching mosquito stats:', err);
        return [];
    }
};


// WebSocket connection
wss.on('connection', async (ws) => {
    console.log('New client connected');

    const sendStats = async () => {
        const stats = await getMosquitoStats();
        ws.send(JSON.stringify(stats));
    };

    sendStats(); // Send initial data

    const interval = setInterval(sendStats, 5000);

    ws.on('close', () => {
        console.log('Client disconnected');
        clearInterval(interval);
    });
});


// API route
app.get('/api/detected-stats', async (req, res) => {
    console.log('Getting api.....');
    const data = await getMosquitoStats();
    res.json(data);
});


server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
