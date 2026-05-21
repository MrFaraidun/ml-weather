const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5000';

app.use(cors());
app.use(express.json());

// Routes
app.get('/models/results', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/results`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch model results' });
  }
});

app.get('/models/best', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/best`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch best model' });
  }
});

app.post('/predict', async (req, res) => {
  try {
    const response = await axios.post(`${ML_SERVICE_URL}/predict`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Prediction failed' });
  }
});

app.get('/status', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/status`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch status' });
  }
});

app.post('/train', async (req, res) => {
  try {
    const response = await axios.post(`${ML_SERVICE_URL}/train`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to start training' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
