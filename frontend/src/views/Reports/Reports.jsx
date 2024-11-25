import React, { useState } from 'react';
import ReportsCard from '../../components/ReportCard/ReportCard';
import Modal from '../../components/Modal/Modal';
import ReportList from '../../components/ReportList/ReportList'; // Importa el nuevo componente
import './Reports.css';

const Reports = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState({ title: '', data: [] });
    const [loading, setLoading] = useState(false); // Para manejar el estado de carga
    const [error, setError] = useState(null); // Para manejar errores

    const reports = [
        {
            title: 'Actividades que más ingresos generan',
            description: 'Se debe sumar el costo de equipamiento.',
            buttonText: 'Ver Reporte',
            endpoint: '/api/reports/income',
            columns: [
                { key: 'actividad', label: 'Actividad' },
                { key: 'ingresos_totales', label: 'Ingresos Totales' },
            ], // Columnas para la tabla del reporte
        },
        {
            title: 'Actividades con más alumnos',
            description: 'Listado de actividades con mayor participación de alumnos.',
            buttonText: 'Ver Reporte',
            endpoint: '/api/reports/popular/activities',
            columns: [
                { key: 'actividad', label: 'Actividad' },
                { key: 'inscripciones', label: 'Cantidad de Alumnos' },
            ],
        },
        {
            title: 'Los turnos con más clases dictadas',
            description: 'Mostrará los turnos con mayor número de clases dictadas.',
            buttonText: 'Ver Reporte',
            endpoint: '/api/reports/popular/shifts',
            columns: [
                { key: 'turno_id', label: 'Turno' },
                { key: 'clases_dictadas', label: 'Clases Dictadas' },
            ],
        },
    ];

    const openModal = async (report) => {
        setLoading(true);
        setError(null);
        setIsModalOpen(true);
        setModalContent({ title: report.title, data: [], columns: report.columns });

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001${report.endpoint}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error fetching report data');
            }

            const data = await response.json();
            if (data.success) {
                setModalContent({ title: report.title, data: data.data, columns: report.columns });
            } else {
                throw new Error(data.message || 'Error desconocido');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setModalContent({ title: '', data: [] });
        setLoading(false);
        setError(null);
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
                {loading ? (
                    <p>Cargando...</p>
                ) : error ? (
                    <p style={{ color: 'red' }}>{error}</p>
                ) : modalContent.data.length > 0 ? (
                    <ReportList data={modalContent.data} columns={modalContent.columns} />
                ) : (
                    <p>No hay datos para mostrar</p>
                )}
            </Modal>
        </div>
    );
};

export default Reports;
