import React, { useState, useEffect } from 'react';
import './Toast.css';

const Toast = ({ message, type, duration, onClose }) => {
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsVisible(false);
            if (onClose) onClose(); 
        }, duration);

        return () => clearTimeout(timer);
    }, [message, duration, onClose]);

    if (!isVisible) return null;

    return (
        <div className={`toast ${type}`}>
            <p>{message}</p>
        </div>
    );
};

export default Toast;
