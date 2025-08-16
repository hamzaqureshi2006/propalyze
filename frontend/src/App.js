import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SearchPage from "./pages/SearchPage";
import PriceEstimator from "./pages/PriceEstimator";
import InvestmentAdvisor from "./pages/InvestmentAdvisor";
import LocationSuggestor from "./pages/LocationSuggestor";
import LocalityAnalyzer from "./pages/LocalityAnalyzer";
import Compare from "./pages/Compare";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AdminPanel from "./pages/AdminPanel";
import PropertyAnalysis from "./pages/PropertyAnalysis";
import PropertyAnalysisForm from "./pages/PropertyAnalysisForm";

import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";
import "./components/layout/Navbar.css";
import "./components/layout/Footer.css";

export default function AppRoutes() {
  return (
    <BrowserRouter>
        <Navbar />
        
        <main style={{ minHeight: "80vh" }}>
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/PropertyAnalysisForm" element={<PropertyAnalysisForm />} />
            <Route path="/PropertyAnalysis" element={<PropertyAnalysis />} />

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
