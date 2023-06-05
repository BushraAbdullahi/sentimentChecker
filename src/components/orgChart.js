import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Chart } from "react-google-charts";

const OrgChart = () => {
  const [ministers, setMinisters] = useState({});

  useEffect(() => {
    axios
      .get('/ministers')
      .then((res) => setMinisters(res.data))
      .catch((err) => console.error(err))
  }, []);

  const [sentiments, setSentiments] = useState({});

  useEffect(() => {
    axios
      .get('/sentiments')
      .then((res) => setSentiments(res.data))
      .catch((err) => console.error(err))
  }, []);

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
        const positive_percentage = getSentimentValue(value.name, 'positive_percentage');
        const neutral_percentage = getSentimentValue(value.name, 'neutral_percentage');
        const negative_percentage = getSentimentValue(value.name, 'negative_percentage');
        
        const data = [
          ['Sentiment', 'Percentage'],
          ['Positive', positive_percentage],
          ['Neutral', neutral_percentage],
          ['Negative', negative_percentage],
        ];
        
        const options = {
          title: 'Sentiment Breakdown',
          colors: ['#006B3D', '#FF980E', '#D3212C'], // positive - green, neutral - yellow, negative - red        
        };

        const hasData = positive_percentage > 0 || neutral_percentage > 0 || negative_percentage > 0;

        return (
          <div className="card" key={key}>
            <div className="circle">
              <img src={value.img_src} alt={value.name} />
            </div>
            <h2>{value.name}</h2>
            <h3>{value.role}</h3>
            {hasData ? (
              <Chart
                chartType="PieChart"
                data={data}
                options={options}
                width={"100%"}
                height={"200px"}
              />
            ) : (
              <div>No Data</div>
            )}
          </div>
        )
      })}
    </div>
  )
}

export default OrgChart;
