import React, { useState } from 'react';
import ReportsCard from '../../components/ReportCard/ReportCard';
import Modal from '../../components/Modal/Modal'; 
import './Reports.css';

const Reports = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState({}); 

    const reports = [
        { 
            title: 'Actividades que mas ingresos generan', 
            description: 'Se debe sumar el costo de equipamiento.', 
            buttonText: 'Ver Reporte' 
        },
        { 
            title: 'Actividades con mas alumnos', 
            description: 'Listado de actividades con mayor participación de alumnos.', 
            buttonText: 'Ver Reporte' 
        },
        { 
            title: 'Los turnos con mas clases dictadas', 
            description: 'Mostrará los turnos con mayor número de clases dictadas.', 
            buttonText: 'Ver Reporte' 
        },
    ];

    const openModal = (report) => {
        setModalContent(report); 
        setIsModalOpen(true); 
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    return (
        <div className="reportsReports">
            <h1 className="reportsReports-title">Reportes</h1>
            <div className="reportsReports-cards">
                {reports.map((report, index) => (
                    <ReportsCard
                        key={index}
                        title={report.title}
                        description={report.description}
                        buttonText={report.buttonText}
                        onButtonClick={() => openModal(report)} 
                    />
                ))}
            </div>

            <Modal isOpen={isModalOpen} onClose={closeModal} title={modalContent.title}>
                <p>{modalContent.description}</p>
            </Modal>
        </div>
    );
};

export default Reports;
