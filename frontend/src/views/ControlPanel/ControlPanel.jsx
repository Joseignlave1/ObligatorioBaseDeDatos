import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../../components/Button/Button';
import PanelCard from '../../components/PanelCard/PanelCard';
import './ControlPanel.css';

const ControlPanel = () => {
    const navigate = useNavigate();

    const categories = [
        { title: 'Actividades', buttonText: 'Ver', path: '/manage-activities' },
        { title: 'Alumnos', buttonText: 'Ver', path: '/manage-students' },
        { title: 'Turnos', buttonText: 'Ver', path: '/manage-shifts' },
        { title: 'Clases', buttonText: 'Ver', path: '/manage-classes' },
        { title: 'Instructores', buttonText: 'Ver', path: '/manage-instructors' },
        { title: 'Reportes', buttonText: 'Ver', path: '/reports' },
        { title: 'Equipamiento', buttonText: 'Ver', path: '/manage-equipments' },
    ];

    const handleButtonClick = (path) => {
        navigate(path);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <div className="control-panel">
            <h1 className="control-panel-title">Panel de Control</h1>
            <div className="control-panel-cards">
                {categories.map((category, index) => (
                    <PanelCard
                        key={index}
                        title={category.title}
                        buttonText={category.buttonText}
                        onButtonClick={() => handleButtonClick(category.path)}
                    />
                ))}
            </div>
            <div className="logout-button-container">
                <Button onClick={handleLogout}>
                    Cerrar Sesion
                </Button>
            </div>
        </div>
    );
};

export default ControlPanel;
