import React from "react";
import "./Loader.css";

export default function Loader({ size = 36, text = "Loading..." }) {
  const style = { width: size, height: size };
  return (
    <div className="loader-wrap" role="status" aria-live="polite">
      <div className="lds-ring" style={style}><div></div><div></div><div></div><div></div></div>
      <div className="loader-text">{text}</div>
    </div>
  );
}
