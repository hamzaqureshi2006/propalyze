import React, { useState, useRef, useEffect} from "react";
import { Link , useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();

  // City tokens input
  const [cities, setCities] = useState(["Ahmedabad"]); // pre-filled example
  const [cityInput, setCityInput] = useState("");
  const cityInputRef = useRef();

  // Property type + BHK
  const [ptypeOpen, setPtypeOpen] = useState(false);
  const [selectedTypes, setSelectedTypes] = useState(["Flat"]);
  const [selectedBhks, setSelectedBhks] = useState(["2 Bhk", "3 Bhk"]);

  // Budget dropdown
  const [budgetOpen, setBudgetOpen] = useState(false);
  const [budget, setBudget] = useState("Any");

  // Close dropdowns when clicking outside
  const ptypeRef = useRef();
  const budgetRef = useRef();

  useEffect(() => {
    function onDocClick(e) {
      if (ptypeRef.current && !ptypeRef.current.contains(e.target)) {
        setPtypeOpen(false);
      }
      if (budgetRef.current && !budgetRef.current.contains(e.target)) {
        setBudgetOpen(false);
      }
    }
    document.addEventListener("click", onDocClick);
    return () => document.removeEventListener("click", onDocClick);
  }, []);

  const addCityToken = (value) => {
    const v = value.trim();
    if (!v) return;
    if (!cities.includes(v)) {
      setCities((s) => [...s, v]);
    }
  };

  const onCityKeyDown = (e) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      addCityToken(cityInput);
      setCityInput("");
    } else if (e.key === "Backspace" && !cityInput && cities.length) {
      // remove last token
      setCities((s) => s.slice(0, s.length - 1));
    }
  };

  const removeCity = (c) => setCities((s) => s.filter((x) => x !== c));

  // property types & BHK chips
  const PROPERTY_TYPES = ["Flat", "House/Villa", "Plot"];
  const BHK_OPTIONS = ["1 Bhk", "2 Bhk", "3 Bhk", "4 Bhk", "5+ Bhk"];

  function toggleType(t) {
    setSelectedTypes((s) =>
      s.includes(t) ? s.filter((x) => x !== t) : [...s, t]
    );
  }
  function toggleBhk(b) {
    setSelectedBhks((s) => (s.includes(b) ? s.filter((x) => x !== b) : [...s, b]));
  }

  // budget options
  const BUDGET_OPTIONS = [
    "Any",
    "Under ₹50L",
    "₹50L - ₹1Cr",
    "₹1Cr - ₹2Cr",
    "₹2Cr+",
  ];

  // Search action (wire to real route / logic)
  const onSearch = () => {
    const payload = {
      cities,
      property_types: selectedTypes,
      bhks: selectedBhks,
      budget,
    };
    // For now just log; replace with navigation / API call
    console.log("Search:", payload);
    // here navigate to search results page , i dont know how to do it

    const params = new URLSearchParams();
    if (cities.length) params.set("cities", cities.join(","));
    if (selectedBhks.length) params.set("bhks", selectedBhks.map(b => b.replace(" Bhk", "")).join(","));
    if (selectedTypes.length) params.set("types", selectedTypes.join(","));
    if (budget && budget !== "Any") params.set("budget", budget.replace(/\s/g, ""));
    navigate(`/search?${params.toString()}`);

  };

  return (
    <header className="topbar">
      <div className="topbar__inner">
        <div className="brand">
          <Link to="/" className="brand__link">
            <span className="brand__logo">Propalyze</span>
          </Link>
        </div>

        <div className="search-pulse">
          <div className="search-pill" role="search" aria-label="Property search">
            {/* Cities token area */}
            <div className="search-segment segment--cities">
              <span className="loc-icon" aria-hidden>📍</span>
              <div className="city-tokens" onClick={() => cityInputRef.current?.focus()}>
                {cities.map((c) => (
                  <span className="city-token" key={c}>
                    {c}
                    <button
                      type="button"
                      className="city-remove"
                      onClick={() => removeCity(c)}
                      aria-label={`Remove ${c}`}
                    >
                      ×
                    </button>
                  </span>
                ))}
                <input
                  ref={cityInputRef}
                  className="city-input"
                  placeholder="Add more..."
                  value={cityInput}
                  onChange={(e) => setCityInput(e.target.value)}
                  onKeyDown={onCityKeyDown}
                />
              </div>
            </div>

            {/* Divider */}
            <div className="search-divider" />

            {/* Property Type Dropdown */}
            <div className="search-segment segment--ptype" ref={ptypeRef}>
              <button
                className="ptype-toggle"
                type="button"
                onClick={() => setPtypeOpen((s) => !s)}
                aria-haspopup="true"
                aria-expanded={ptypeOpen}
              >
                <span role="img" aria-hidden>🏠</span>
                <span className="ptype-label">
                  {selectedTypes.length === 0 ? "Property" : selectedTypes.join(", ")}
                </span>
                <span className="caret">▾</span>
              </button>

              {ptypeOpen && (
                <div className="ptype-panel" role="dialog" aria-label="Property type selector">
                  <div className="ptype-section">
                    <div className="ptype-section-title">Residential</div>
                    <div className="chip-row">
                      {PROPERTY_TYPES.map((t) => (
                        <button
                          key={t}
                          type="button"
                          className={`chip ${selectedTypes.includes(t) ? "chip--active" : ""}`}
                          onClick={() => toggleType(t)}
                        >
                          {t}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="ptype-section">
                    <div className="ptype-section-title">BHK</div>
                    <div className="chip-row">
                      {BHK_OPTIONS.map((b) => (
                        <button
                          key={b}
                          type="button"
                          className={`chip ${selectedBhks.includes(b) ? "chip--active" : ""}`}
                          onClick={() => toggleBhk(b)}
                        >
                          {b}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="search-divider" />

            {/* Budget Dropdown */}
            <div className="search-segment segment--budget" ref={budgetRef}>
              <button
                className="budget-toggle"
                type="button"
                onClick={() => setBudgetOpen((s) => !s)}
                aria-haspopup="true"
                aria-expanded={budgetOpen}
              >
                <span role="img" aria-hidden>₹</span>
                <span className="budget-label">{budget}</span>
                <span className="caret">▾</span>
              </button>

              {budgetOpen && (
                <div className="budget-panel" role="menu" aria-label="Budget options">
                  {BUDGET_OPTIONS.map((opt) => (
                    <div key={opt} className="budget-row">
                      <label>
                        <input
                          type="radio"
                          name="budget"
                          checked={budget === opt}
                          onChange={() => setBudget(opt)}
                        />
                        <span className="budget-text">{opt}</span>
                      </label>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Search button */}
            <div className="search-segment segment--action">
              <button className="search-button" onClick={onSearch} aria-label="Search properties">
                🔍 <span className="search-text">Search</span>
              </button>
            </div>
          </div>
        </div>

        <nav className="top-actions">
          <Link to="/about" className="top-link">About</Link>
          <Link to="/contact" className="top-link">Contact</Link>
          <Link to="/login" className="top-cta">Login</Link>
          <Link to="/signup" className="top-cta signup">Sign up</Link>
        </nav>
      </div>
    </header>
  );
}
