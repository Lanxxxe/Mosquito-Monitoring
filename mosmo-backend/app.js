require('dotenv').config();

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

app.use(cors({
    origin: 'https://mosmo.vercel.app/',
    methods: ['GET', 'POST'],
    credentials: true
}));

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

const getMosquitoStats = async () => {
    try {
        const totalDetections = await MosquitoDetection.countDocuments();
        const detectionCounts = await MosquitoDetection.aggregate([
            {
                $group: {
                    _id: "$species_name",
                    detected_count: { $sum: 1 }
                }
            }
        ]);

        const mosquitoes = await Mosquito.find();
        const diseases = await Disease.find();
        const mosquitoStats = detectionCounts.map(detection => {
            const mosquitoInfo = mosquitoes.find(m => m.name === detection._id);
            
            if (!mosquitoInfo) return null;

            const diseaseNames = mosquitoInfo.diseases.map(diseaseId => {
                const disease = diseases.find(d => d._id.equals(diseaseId));
                return disease ? disease.name : null;
            }).filter(Boolean).join(', ');

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


// API route
app.get('/api/detected-stats', async (req, res) => {
    console.log('Getting api.....');
    const data = await getMosquitoStats();
    res.json(data);
});

module.exports = app;
