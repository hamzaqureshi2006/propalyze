import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Loader from "../components/layout/Loader";
import "./SearchPage.css";

/**
 * SearchPage
 * - Reads URL params: bhks, cities, types, budget
 * - Calls POST /api/search with payload { bhks: [], cities: [], property_types: [], budget_min, budget_max }
 * - If API fails, falls back to dummy data (2 items)
 */

function parseCSVParam(value) {
  if (!value) return [];
  return value
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

function parseBudget(budgetStr) {
  if (!budgetStr) return { min: null, max: null };
  // Common formats: "Any", "Under ₹50L", "₹50L - ₹1Cr", "500000-2000000"
  if (budgetStr.toLowerCase() === "any") return { min: null, max: null };

  // try "min-max" numeric
  if (budgetStr.includes("-")) {
    const parts = budgetStr.split("-").map((p) => p.replace(/[^\d]/g, "").trim());
    const min = parts[0] ? parseInt(parts[0], 10) : null;
    const max = parts[1] ? parseInt(parts[1], 10) : null;
    return { min, max };
  }

  // fallback: not parseable
  return { min: null, max: null };
}

const DUMMY_RESULTS = [
  {
    id: "dummy-1",
    title: "Spacious 2 BHK in Central Locality",
    city: "Bengaluru",
    locality: "Koramangala",
    bhk: 2,
    area: 950,
    price: 8500000,
    image_url: "https://via.placeholder.com/320x200?text=Property+1",
  },
  {
    id: "dummy-2",
    title: "Modern 3 BHK with amenities",
    city: "Mumbai",
    locality: "Andheri West",
    bhk: 3,
    area: 1200,
    price: 14500000,
    image_url: "https://via.placeholder.com/320x200?text=Property+2",
  },
];

export default function SearchPage() {
  const { search } = useLocation();
  const [results, setResults] = useState(null); // null = loading not started, [] = loaded no items
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    let cancelled = false;

    // parse query params
    const params = new URLSearchParams(search);

    const bhks = parseCSVParam(params.get("bhks")).map((b) => {
      // try to extract number from "2" or "2 Bhk"
      const m = b.match(/\d+/);
      return m ? parseInt(m[0], 10) : b;
    });
    const cities = parseCSVParam(params.get("cities"));
    const types = parseCSVParam(params.get("types"));
    const budgetRaw = params.get("budget") || params.get("price") || "";
    const { min: budget_min, max: budget_max } = parseBudget(budgetRaw);

    const payload = {
      bhks,
      cities,
      property_types: types,
    };
    if (budget_min != null) payload.budget_min = budget_min;
    if (budget_max != null) payload.budget_max = budget_max;

    async function doSearch() {
      setLoading(true);
      setErrorMsg("");
      setResults(null);
      try {
        // call backend search API
        const res = await fetch("/api/search", {
          method: "POST",
          credentials: "include", // send cookies
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!res.ok) {
          throw new Error(`Server returned ${res.status}`);
        }

        const data = await res.json();

        // backend shape may vary; adapt as needed
        // if backend returns { results: [...] } or just [...]
        const items = Array.isArray(data)
          ? data
          : data.results || data.items || [];

        if (!cancelled) {
          setResults(items);
        }
      } catch (err) {
        console.warn("Search API failed — using dummy data:", err);
        if (!cancelled) {
          setErrorMsg(
            "Live search is unavailable — showing example results (backend not ready)."
          );
          setResults(DUMMY_RESULTS);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    doSearch();

    return () => {
      cancelled = true;
    };
  }, [search]);

  return (
    <div className="search-root">
      <header className="search-header">
        <h1>Search Results</h1>
        <p className="search-sub">
          Results based on your filters. Adjust filters in the search bar or via query params.
        </p>
      </header>

      {loading ? (
        <div className="search-loading">
          <Loader size={36} text="Searching properties..." />
        </div>
      ) : (
        <>
          {errorMsg && <div className="search-error">{errorMsg}</div>}

          {Array.isArray(results) && results.length === 0 ? (
            <div className="search-empty">
              <h3>No properties found</h3>
              <p>Try broadening your search — remove city or increase budget.</p>
            </div>
          ) : (
            <div className="results-grid">
              {results.map((p) => (
                <article key={p.id || p.property_id || `${p.city}-${p.locality}-${p.bhk}`} className="property-card">
                  <div className="property-media">
                    <img src={p.image_url || p.photo || "https://via.placeholder.com/320x200?text=No+Image"} alt={p.title || `${p.bhk} BHK in ${p.locality}`} />
                  </div>
                  <div className="property-body">
                    <h3 className="property-title">{p.title || `${p.bhk} BHK in ${p.locality}`}</h3>
                    <div className="property-meta">
                      <span>{p.city} · {p.locality}</span>
                      <span>{p.bhk} BHK · {p.area ? `${p.area} sqft` : "Area N/A"}</span>
                    </div>
                    <div className="property-price">₹ {p.price ? p.price.toLocaleString() : "Contact"}</div>
                    <div className="property-actions">
                      <button className="btn">Estimate Price</button>
                      <button className="btn outline">Analyze Locality</button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
