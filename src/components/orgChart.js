import React, { useState, useEffect } from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'

// Define a component named OrgChart.
const OrgChart = () => {
  // // Declare state variables.
  const [ministers, setMinisters] = useState({})

  useEffect(() => {
    axios
      .get('http://localhost:5000/')
      .then((res) => setMinisters(res.data))
      .catch((err) => console.error(err))
  }, [])

  // // Declare a state variable.
  const [sentiments, setSentiments] = useState({})

  useEffect(() => {
    axios
      .get('http://localhost:5000/sentiments')
      .then((res) => setSentiments(res.data))
      .catch((err) => console.error(err))
  }, [])

  function getSentimentValue(key, sentiment) {
    if (sentiments[key] && sentiments[key][sentiment]) {
      return sentiments[key][sentiment]
    }
    return null
  }

  return (
    <div className="org-chart">
      {Object.entries(ministers).map(([key, value], index) => (
        <div className="card" key={key}>
          <div className="circle">
            <img src={value.img_src} alt={value.name} />
          </div>
          <h2>{value.name}</h2>
          <h3>{value.role}</h3>
          <div className="progress" style={{ maxWidth: '50%' }}>
            <div class="progress-bar bg-success" style={{ width: String(getSentimentValue(value.name, 'positive_percentage')) }}>
            {getSentimentValue(value.name, 'positive_percentage')}
            </div>
            <div class="progress-bar bg-warning" style={{ width: String(getSentimentValue(value.name, 'neutral_percentage')) }}>
            {getSentimentValue(value.name, 'neutral_percentage')}
            </div>
            <div class="progress-bar bg-danger" style={{ width: String(getSentimentValue(value.name, 'negative_percentage')) }}>
            {getSentimentValue(value.name, 'negative_percentage')}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default OrgChart
