import React from "react";
import { Link, NavLink } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar__logo">
        <Link to="/">Propalyze</Link>
      </div>
      <ul className="navbar__links">
        <li><NavLink to="/" end>Home</NavLink></li>
        <li><NavLink to="/price-estimator">Price Estimator</NavLink></li>
        <li><NavLink to="/investment-advisor">Investment Advisor</NavLink></li>
        <li><NavLink to="/smart-location-suggestor">Smart Location</NavLink></li>
        <li><NavLink to="/compare-property">Compare</NavLink></li>
        <li><NavLink to="/login">Login</NavLink></li>
      </ul>
    </nav>
  );
};

export default Navbar;