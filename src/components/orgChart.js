import React from 'react';
// import sunak from 'src/assets/sunak.jpeg';


const OrgChart = () => {
  return (
    <div className="org-chart">

      <div className="card">
        <div className="circle">
          {/* <img src={sunak} alt="sunak" /> */}
        </div>
        <h2>Rishi Sunak</h2>
        <h3>Prime Minister of the United Kingdom</h3>
      </div>

      {/* <div className="card">
        <div className="circle">
          <img src="person2.jpg" alt="Person 2" />
        </div>
        <p>Person 2</p>
      </div> */}
      
      {/* Add more cards for other people in the org chart */}
    </div>
  );
};

export default OrgChart;