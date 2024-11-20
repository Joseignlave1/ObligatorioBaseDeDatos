import React from 'react';
import './ReportCard.css';

const ReportCard = ({ title, description, buttonText, onButtonClick }) => {
    return (
        <div className="report-card">
            <div className="report-card-header">
                <h3 className="report-card-title">{title}</h3>
            </div>
            <div className="report-card-body">
                <p className="report-card-description">{description}</p>
            </div>
            <div className="report-card-aside">
                <button className="report-card-button" onClick={onButtonClick}>
                    {buttonText}
                </button>
            </div>
        </div>
    );
};

export default ReportCard;
