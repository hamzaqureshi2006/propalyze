import React from "react";
import "./Footer.css";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div className="footer-left">
          <div className="footer-brand">Propalyze</div>
          <div className="footer-tag">AI-powered real estate insights</div>
        </div>

        <div className="footer-links">
          <a href="/about">About Us</a>
          <a href="/contact">Contact</a>
          <a href="/terms">Terms</a>
          <a href="/privacy">Privacy</a>
        </div>

        <div className="footer-right">
          <small>© {new Date().getFullYear()} Propalyze</small>
        </div>
      </div>
    </footer>
  );
}
