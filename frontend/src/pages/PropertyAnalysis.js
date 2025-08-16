import React, { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

const PropertyAnalysis = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Example API call
    axios
      .get("/api/property-analysis", { params: { propertyId: 123 } })
      .then((res) => setData(res.data))
      .catch(() => {
        // Dummy fallback data
        setData({
          predictedPrice: 85_00_000, // ₹85 Lakh
          locality: {
            nearby: {
              schools: 5,
              hospitals: 3,
              shops: 12,
              transport: 4,
            },
            environment: {
              aqi: 112,
              mosquitoIndex: "Moderate",
              noiseLevel: "High",
              temperature: "28°C",
            },
            other: {
              traffic: "Heavy",
              safetyIndex: "Low crime rate",
            },
          },
          investment: {
            history: [
              { month: "Sep", price: 78 },
              { month: "Oct", price: 80 },
              { month: "Nov", price: 82 },
              { month: "Dec", price: 79 },
              { month: "Jan", price: 81 },
              { month: "Feb", price: 84 },
              { month: "Mar", price: 86 },
              { month: "Apr", price: 85 },
              { month: "May", price: 88 },
              { month: "Jun", price: 87 },
              { month: "Jul", price: 90 },
              { month: "Aug", price: 92 },
            ],
            recommendation: "Good time to invest. Prices have shown consistent growth (avg 5% YoY).",
          },
        });
      });
  }, []);

  if (!data) return <h2>Loading Property Analysis...</h2>;

  return (
    <div className="analysis-container">
      {/* 1. Predicted Price */}
      <section className="predicted-price">
        <h2>🏠 Predicted Price</h2>
        <p className="price">₹ {data.predictedPrice.toLocaleString()}</p>
      </section>

      {/* 2. Locality Analysis */}
      <section className="locality-analysis">
        <h2>📍 Locality Analysis</h2>

        <div className="sub-section">
          <h3>Nearby Facilities</h3>
          <ul>
            <li>Schools: {data.locality.nearby.schools}</li>
            <li>Hospitals: {data.locality.nearby.hospitals}</li>
            <li>Shops: {data.locality.nearby.shops}</li>
            <li>Transport: {data.locality.nearby.transport}</li>
          </ul>
        </div>

        <div className="sub-section">
          <h3>Environmental Details</h3>
          <ul>
            <li>Air Quality Index: {data.locality.environment.aqi}</li>
            <li>Mosquito Index: {data.locality.environment.mosquitoIndex}</li>
            <li>Noise Level: {data.locality.environment.noiseLevel}</li>
            <li>Temperature: {data.locality.environment.temperature}</li>
          </ul>
        </div>

        <div className="sub-section">
          <h3>Other Details</h3>
          <ul>
            <li>Traffic: {data.locality.other.traffic}</li>
            <li>Safety: {data.locality.other.safetyIndex}</li>
          </ul>
        </div>
      </section>

      {/* 3. Investment Section */}
      <section className="investment-section">
        <h2>📈 Investment Insights</h2>

        <div style={{ width: "100%", height: 300 }}>
          <ResponsiveContainer>
            <LineChart data={data.investment.history}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="price" stroke="#007BFF" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <p className="recommendation">{data.investment.recommendation}</p>
      </section>
    </div>
  );
};

export default PropertyAnalysis;
