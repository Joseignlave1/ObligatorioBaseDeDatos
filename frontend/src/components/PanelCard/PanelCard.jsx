import React from 'react';
import './PanelCard.css';

const PanelCard = ({ title, buttonText, onButtonClick }) => {
    return (
        <div className="panel-card">
            <h3 className="panel-card-title">{title}</h3>
            <button className="panel-card-button" onClick={onButtonClick}>
                {buttonText}
            </button>
        </div>
    );
};

export default PanelCard;
