import React, { useState, useEffect } from 'react'
import axios from 'axios'
import '../appHeader.css'

// Define a component named OrgChart.
const Header = () => {
  // Declare state variables.
  const [displayDate, setDisplayDate] = useState("");
  useEffect(() => {
    axios
      .get('/display_date')
      .then((res) => setDisplayDate(res.data))
      .catch((err) => console.error(err))
  }, [])

  return (
    <div className="appHeader">
      <div className="headerContent">
        <h1>Government Minister Sentiment Analysis</h1>
        <h2>{displayDate}</h2>
        <p>This chart displays sentiment analysis of tweets from various government ministers.</p>
      </div>
    </div>
  )
}

export default Header
