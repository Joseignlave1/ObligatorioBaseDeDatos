import React from 'react';
import './Input.css'; 

const Input = ({ placeholder, value, onChange, type = 'text' }) => {
    return (
        <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
        />
    );
};

export default Input;
