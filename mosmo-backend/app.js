require('dotenv').config();

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const port = 5000;

app.use(cors({
    origin: ['https://mosmo-lances-projects-1e037f69.vercel.app/', 'https://mosmo.vercel.app/', 'http://localhost:5173'],
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
                    detected_count: { $sum: 1 },
                    last_detected_time: { $max: "$detection_time" }
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

            const formattedTime = detection.last_detected_time
                ? new Date(detection.last_detected_time).toLocaleString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true
                })
                : null;


            return {
                mosquito_name: mosquitoInfo.name,
                mosquito_description: mosquitoInfo.description,
                diseases: diseaseNames,
                detected_count: detection.detected_count,
                detected_percentage: parseFloat(detected_percentage),
                last_detected_time: formattedTime
            };
        }).filter(Boolean);

        return { rows: mosquitoStats };
    } catch (err) {
        console.error('Error fetching mosquito stats:', err);
        return [];
    }
};

async function getMosquitoLogs(speciesName) {
    try {
      const logs = await MosquitoDetection.find({ species_name: speciesName })
        .sort({ detection_time: -1 })
        .select("detection_time -_id");
  
      const formattedLogs = logs.map((log) => ({
        detected_time: new Date(log.detection_time).toLocaleString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "numeric",
          minute: "2-digit",
          hour12: true,
        }),
      }));
  
      return { species_name: speciesName, logs: formattedLogs };
    } catch (err) {
      console.error("Error in getMosquitoLogs:", err);
      throw err;
    }
  }


app.get('/api/mosquito/logs/:species', async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', 'https://mosmo.vercel.app');
    try {
      const speciesName = req.params.species;
      const data = await getMosquitoLogs(speciesName);
      res.json(data);
    } catch (err) {
      console.error("Error fetching mosquito logs:", err);
      res.status(500).json({ error: "Internal Server Error" });
    }
});


app.get('/api/detected-stats', async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', 'https://mosmo.vercel.app');
    const data = await getMosquitoStats();
    res.json(data);
});

module.exports = app;
// app.listen(port, () => {
//   console.log(`Server running on http://localhost:${port}`);
// });
