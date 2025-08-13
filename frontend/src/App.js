import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PriceEstimator from "./pages/PriceEstimator";
import InvestmentAdvisor from "./pages/InvestmentAdvisor";
import LocationSuggestor from "./pages/LocationSuggestor";
import LocalityAnalyzer from "./pages/LocalityAnalyzer";
import Compare from "./pages/Compare";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AdminPanel from "./pages/AdminPanel";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./App.css";

export default function AppRoutes() {
  return (
    <BrowserRouter>
        <Navbar />
        <main style={{ minHeight: "80vh" }}>
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/price-estimator" element={<PriceEstimator />} />
            <Route path="/investment-advisor" element={<InvestmentAdvisor />} />
            <Route path="/location-suggestor" element={<LocationSuggestor />} />
            <Route path="/locality-analyzer" element={<LocalityAnalyzer />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/admin" element={<AdminPanel />} />
        </Routes>
        </main>
        <Footer />
    </BrowserRouter>
  );
}
