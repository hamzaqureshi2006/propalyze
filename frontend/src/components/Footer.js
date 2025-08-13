import React from "react";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <p>© {new Date().getFullYear()} Propalyze. All rights reserved.</p>
      <p>
        Built with ❤️ for smarter real estate decisions.
      </p>
    </footer>
  );
};

export default Footer;