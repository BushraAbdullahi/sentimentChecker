import React, { useState, useEffect } from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import { PieChart } from 'react-minimal-pie-chart'

// Define a component named OrgChart.
const OrgChart = () => {
  // Declare state variables.
  const [ministers, setMinisters] = useState({})

  useEffect(() => {
    axios
      .get('https://sentiment-checker.herokuapp.com/ministers')
      .then((res) => setMinisters(res.data))
      .catch((err) => console.error(err))
  }, [])

  // Declare a state variable.
  const [sentiments, setSentiments] = useState({})

  useEffect(() => {
    axios
      .get('https://sentiment-checker.herokuapp.com/sentiments')
      .then((res) => setSentiments(res.data))
      .catch((err) => console.error(err))
  }, [])

  function getSentimentValue(key, sentiment) {
    if (sentiments[key] && sentiments[key][sentiment]) {
      return sentiments[key][sentiment]
    } else {
      return 0
    }
  }

  return (
    <div className="org-chart">
      {Object.entries(ministers).map(([key, value], index) => {
        const positive_percentage = getSentimentValue(
          value.name,
          'positive_percentage',
        )
        const neutral_percentage = getSentimentValue(
          value.name,
          'neutral_percentage',
        )
        const negative_percentage = getSentimentValue(
          value.name,
          'negative_percentage',
        )
        const hasData =
          positive_percentage > 0 ||
          neutral_percentage > 0 ||
          negative_percentage > 0

        return (
          <div className="card" key={key}>
            <div className="circle">
              <img src={value.img_src} alt={value.name} />
            </div>
            <h2>{value.name}</h2>
            <h3>{value.role}</h3>
            <div className="pie-chart">
              {hasData ? (
                <PieChart
                  data={[
                    {
                      title: 'Positive Percentage: ' + positive_percentage,
                      value: positive_percentage,
                      color: '#ABFF77',
                    },
                    {
                      title: 'Neutral Percentage: ' + neutral_percentage,
                      value: neutral_percentage,
                      color: '#FFED78',
                    },
                    {
                      title: 'Negative Percentage: ' + negative_percentage,
                      value: negative_percentage,
                      color: '#FF7878',
                    },
                  ]}
                />
              ) : (
                <div>No Data</div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default OrgChart
