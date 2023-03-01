import React, { useState, useEffect } from "react";
import axios from "axios";

// Define a component named OrgChart.
const OrgChart = () => {
  // // Declare a state variable.  
    const [data, setData] = useState({});
  
    useEffect(() => {
      axios
        .get("http://localhost:5000/")
        .then(res => setData(res.data))
        .catch(err => console.error(err));
    }, []);

    return (
      <div className="org-chart">
        {Object.entries(data).map(([key, value], index) => (
          <div className="card" key={key}>
            <div className="circle">
              <img src={value.img_src} alt={value.name} />
            </div>
            <h2>{value.name}</h2>
            <h3>{value.role}</h3>
          </div>
        ))}
      </div>
    );
};

export default OrgChart;