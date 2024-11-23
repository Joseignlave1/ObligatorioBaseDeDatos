import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Table from '../../components/Table/Table';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import Modal from '../../components/Modal/Modal';
import './ManageShifts.css';

const ManageShifts = () => {
    const navigate = useNavigate();

    const [shifts, setShifts] = useState([]);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newShiftStartTime, setNewShiftStartTime] = useState('');
    const [newShiftEndTime, setNewShiftEndTime] = useState('');
    const [formError, setFormError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedShiftId, setSelectedShiftId] = useState(null);

    const fetchShifts = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/shifts/all', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error fetching shifts');
            }

            const data = await response.json();
            setShifts(data);
        } catch (err) {
            setError(err.message);
            console.error(err);
        }
    };

    useEffect(() => {
        fetchShifts();
    }, []);

    if (error) {
        return <div>{error}</div>;
    }

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };
    const handleModal = (isEditingMode = false, shift = null) => {
        setFormError(null);
        setIsModalOpen(true);
        setIsEditing(isEditingMode);

        if (isEditingMode && shift) {
            setSelectedShiftId(shift.id);

            // Función para convertir AM/PM a formato de 24 horas (HH:mm)
            const formatTimeTo24Hour = (time) => {
                // Verifica si el formato es AM/PM
                const match = time.match(/(\d+):(\d+)\s?(AM|PM)/i);
                if (!match) {
                    // Si ya está en formato HH:mm, simplemente lo retornamos
                    return time;
                }
                let [_, hour, minute, meridian] = match;
                hour = parseInt(hour, 10);
                if (meridian.toUpperCase() === "PM" && hour !== 12) {
                    hour += 12;
                }
                if (meridian.toUpperCase() === "AM" && hour === 12) {
                    hour = 0;
                }
                return `${String(hour).padStart(2, "0")}:${minute}`;
            };

            // Convierte las horas al formato HH:mm si es necesario
            const start_time = formatTimeTo24Hour(shift.hora_inicio);
            const end_time = formatTimeTo24Hour(shift.hora_fin);

            console.log("Hora inicio convertida:", start_time); // Depuración
            console.log("Hora fin convertida:", end_time); // Depuración

            setNewShiftStartTime(start_time);
            setNewShiftEndTime(end_time);
        } else {
            setSelectedShiftId(null);
            setNewShiftStartTime('');
            setNewShiftEndTime('');
        }
    };





    const handleAddShift = async () => {
        setFormError(null);

        if (!newShiftStartTime || !newShiftEndTime) {
            setFormError('Todos los campos son requeridos');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/shifts', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start_time: newShiftStartTime,
                    end_time: newShiftEndTime,
                }),
            });

            if (!response.ok) {
                throw new Error('Error al guardar el turno');
            }

            await response.json();
            setIsModalOpen(false);
            fetchShifts();
        } catch (err) {
            setFormError(err.message);
            console.error(err);
        }
    };

    const handleEditShift = async () => {
        setFormError(null);

        if (!newShiftStartTime || !newShiftEndTime) {
            setFormError('Todos los campos son requeridos');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001/api/shifts/${selectedShiftId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start_time: newShiftStartTime,
                    endt_time: newShiftEndTime,
                }),
            });

            if (!response.ok) {
                throw new Error('Error al actualizar el turno');
            }

            await response.json();
            setIsModalOpen(false);
            fetchShifts();
        } catch (err) {
            setFormError(err.message);
            console.error(err);
        }
    };

    const handleDeleteShift = async (shiftId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001/api/shifts/${shiftId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error al eliminar el turno');
            }

            await response.json();
            fetchShifts();
        } catch (err) {
            console.error(err.message);
            setError('No se pudo eliminar el turno');
        }
    };

    const filteredShifts = shifts.filter((shift) => {
    return (
        (shift.hora_inicio && shift.hora_inicio.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (shift.hora_fin && shift.hora_fin.toLowerCase().includes(searchTerm.toLowerCase()))
    );
});


    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'hora_inicio', label: 'Hora de Inicio' },
        { key: 'hora_fin', label: 'Hora de Fin' },
    ];

    return (
        <div className="manageShifts">
            <Button onClick={() => navigate('/control-panel')}>
                Atrás
            </Button>
            <h1 className="manageShifts-title">Gestionar Turnos</h1>
            <div className="manageShifts-table">
                <div className="manageShifts-search">
                    <Input
                        placeholder="Buscar turno..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                    />
                    <Button color="#f0ad4e" onClick={() => handleModal(false)}>Agregar</Button>
                </div>
                <Table
                    data={filteredShifts}
                    columns={columns}
                    onEdit={(shift) => handleModal(true, shift)}
                    onDelete={(shift) => handleDeleteShift(shift.id)}
                />
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={isEditing ? "Editar Turno" : "Agregar Turno"}
            >
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        isEditing ? handleEditShift() : handleAddShift();
                    }}
                    className="modal-form"
                >
                    {formError && <div className="error-message">{formError}</div>}

                    <div className="form-group">
                        <label>Hora de Inicio</label>
                        <Input
                            type="time"
                            placeholder="Hora de inicio"
                            value={newShiftStartTime}
                            onChange={(e) => setNewShiftStartTime(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>Hora de Fin</label>
                        <Input
                            type="time"
                            placeholder="Hora de fin"
                            value={newShiftEndTime}
                            onChange={(e) => setNewShiftEndTime(e.target.value)}
                        />
                    </div>

                    <div className="form-actions">
                        <Button type="submit" color="#4CAF50">
                            {isEditing ? 'Actualizar Turno' : 'Crear Turno'}
                        </Button>
                        <Button type="button" color="#f44336" onClick={() => setIsModalOpen(false)}>Cancelar</Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default ManageShifts;
