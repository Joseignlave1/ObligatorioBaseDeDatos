import React from 'react';
import Button from '../Button/Button';
import './Table.css';

const Table = ({ data, columns, onEdit, onDelete }) => {
    if (!data || data.length === 0) {
        return <p className="table-no-data">No data available.</p>;
    }

    return (
        <table className="table">
            <thead>
                <tr>
                    {columns.map((column) => (
                        <th key={column.key} className="table-header">{column.label}</th>
                    ))}
                    <th className="table-header">Acciones</th> 
                </tr>
            </thead>
            <tbody>
                {data.map((row, index) => (
                    <tr key={index} className="table-row">
                        {columns.map((column) => (
                            <td key={column.key} className="table-cell">{row[column.key]}</td>
                        ))}
                        <td className="table-cell">
                            <Button onClick={() => onEdit(row)} color="#4CAF50">Edit</Button> {/* Verde */}
                            <Button onClick={() => onDelete(row)} color="#f44336">Delete</Button> {/* Rojo */}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default Table;



