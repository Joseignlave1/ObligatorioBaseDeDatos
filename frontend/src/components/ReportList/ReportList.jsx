import React from 'react';
import './ReportList.css';

const ReportList = ({ data, columns }) => {
    if (!data || data.length === 0) {
        return <p className="report-list-no-data">No hay datos disponibles.</p>;
    }

    return (
        <div className="report-list">
            {data.map((item, index) => (
                <div key={index} className="report-list-item">
                    {/* Número del ranking */}
                    <div className="report-list-rank">
                        #{index + 1}
                    </div>

                    {/* Datos del reporte */}
                    <div className="report-list-data">
                        {columns.map((column) => (
                            <div key={column.key} className="report-list-field">
                                <span className="report-list-label">{column.label}:</span>
                                <span className="report-list-value">{item[column.key]}</span>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ReportList;
