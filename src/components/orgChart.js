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
      return sentiments[key][sentiment];
    }
    return null;
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
          <div className="progress" style={{ maxWidth: '60%' }}>
            <div
              className="progress-bar"
              style={{ width: getSentimentValue(key, "positive_percentage"), backgroundColor: '#018a16' }}
            >
              {getSentimentValue(key, "positive_percentage")}
              {console.log(getSentimentValue(key, "positive_percentage"))}
            </div>
            <div
              className="progress-bar"
              style={{ width: getSentimentValue(key, "neutral_percentage"), backgroundColor: '#ded414' }}
            >
              {getSentimentValue(key, "neutral_percentage")}
            </div>
            <div
              className="progress-bar"
              style={{ width: getSentimentValue(key, "negative_percentage"), backgroundColor: '#ad0202' }}
            >
              {getSentimentValue(key, "negative_percentage")}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default OrgChart
