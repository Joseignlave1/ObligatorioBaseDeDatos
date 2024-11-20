import React from 'react';
import './Button.css';

const Button = ({ children, onClick, color }) => {
    return (
        <button 
            className="button" 
            onClick={onClick} 
            style={{ backgroundColor: color }}
        >
            {children}
        </button>
    );
};

export default Button;
