import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const Home = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    city: "",
    locality: "",
    propertyType: "",
    bhk: "",
    area: "",
    budget: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Redirect to property analysis with query params
    const query = new URLSearchParams(form).toString();
    navigate(`/PropertyAnalysis?${query}`);
  };

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero">
        <h1>🏡 Find Your Property's True Worth</h1>
        <p>
          Estimate prices, analyze locality, and get smart investment insights —
          all in one place.
        </p>
      </section>

      {/* Quick Property Analysis Form */}
      <section className="quick-form">
        <h2>🔍 Quick Property Analysis</h2>
        <form onSubmit={handleSubmit} className="form-grid">
          <input
            type="text"
            name="city"
            placeholder="City"
            value={form.city}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="locality"
            placeholder="Locality"
            value={form.locality}
            onChange={handleChange}
            required
          />
          <select name="propertyType" value={form.propertyType} onChange={handleChange} required>
            <option value="">Select Property Type</option>
            <option value="Apartment">Apartment</option>
            <option value="SingleFamilyResidence">Single Family</option>
            <option value="Plot">Plot</option>
          </select>
          <select name="bhk" value={form.bhk} onChange={handleChange} required>
            <option value="">BHK</option>
            <option value="1">1 BHK</option>
            <option value="2">2 BHK</option>
            <option value="3">3 BHK</option>
            <option value="4">4+ BHK</option>
          </select>
          <input
            type="number"
            name="area"
            placeholder="Area (sq ft)"
            value={form.area}
            onChange={handleChange}
          />
          <input
            type="number"
            name="budget"
            placeholder="Budget (₹)"
            value={form.budget}
            onChange={handleChange}
          />
          <button type="submit">Analyze</button>
        </form>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2>✨ What You Can Do Here</h2>
        <div className="feature-grid">
          <div className="feature-card">
            <h3>💰 Price Estimator</h3>
            <p>Predict your property’s current market value instantly.</p>
          </div>
          <div className="feature-card">
            <h3>📍 Locality Analysis</h3>
            <p>See nearby schools, hospitals, transport, and safety stats.</p>
          </div>
          <div className="feature-card">
            <h3>📈 Investment Insights</h3>
            <p>Check price trends and decide the best time to invest.</p>
          </div>
          <div className="feature-card">
            <h3>🔗 Saved & Compare</h3>
            <p>Save properties and compare them before making decisions.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
