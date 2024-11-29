import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Table from '../../components/Table/Table';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import Modal from '../../components/Modal/Modal';
import './ManageEquipment.css';

const ManageEquipment = () => {
    const navigate = useNavigate();

    const [equipment, setEquipment] = useState([]);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newEquipmentDescription, setNewEquipmentDescription] = useState('');
    const [newEquipmentCost, setNewEquipmentCost] = useState('');
    const [selectedActivityId, setSelectedActivityId] = useState('');
    const [formError, setFormError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedEquipmentId, setSelectedEquipmentId] = useState(null);

    const fetchEquipment = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/equipment/all', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error fetching equipment');
            }

            const data = await response.json();
            setEquipment(data);
        } catch (err) {
            setError(err.message);
            console.error(err);
        }
    };

    useEffect(() => {
        fetchEquipment();
    }, []);

    if (error) {
        return <div>{error}</div>;
    }

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleModal = (isEditingMode = false, equipment = null) => {
        setFormError(null);
        setIsModalOpen(true);
        setIsEditing(isEditingMode);

        if (isEditingMode && equipment) {
            setSelectedEquipmentId(equipment.id);
            setNewEquipmentDescription(equipment.descripcion || '');
            setNewEquipmentCost(equipment.costo || '');
            setSelectedActivityId(equipment.id_actividad || '');
        } else {
            setSelectedEquipmentId(null);
            setNewEquipmentDescription('');
            setNewEquipmentCost('');
            setSelectedActivityId('');
        }
    };

    const handleAddEquipment = async () => {
        setFormError(null);

        if (!newEquipmentDescription || !newEquipmentCost || !selectedActivityId) {
            setFormError('Todos los campos son requeridos');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/equipment/add', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    description: newEquipmentDescription,
                    cost: parseFloat(newEquipmentCost),
                    activity_id: parseInt(selectedActivityId),
                }),
            });

            if (!response.ok) {
                throw new Error('Error al guardar el equipamiento');
            }

            await response.json();
            setIsModalOpen(false);
            fetchEquipment();
        } catch (err) {
            setFormError(err.message);
            console.error(err);
        }
    };

    const handleEditEquipment = async () => {
        setFormError(null);

        if (!newEquipmentDescription || !newEquipmentCost || !selectedActivityId) {
            setFormError('Todos los campos son requeridos');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001/api/equipment/modify/${selectedEquipmentId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    description: newEquipmentDescription,
                    cost: parseFloat(newEquipmentCost),
                    activity_id: parseInt(selectedActivityId),
                }),
            });

            if (!response.ok) {
                throw new Error('Error al actualizar el equipamiento');
            }

            await response.json();
            setIsModalOpen(false);
            fetchEquipment();
        } catch (err) {
            setFormError(err.message);
            console.error(err);
        }
    };


    const handleDeleteEquipment = async (equipmentId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001/api/equipment/delete/${equipmentId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error al eliminar el equipamiento');
            }

            await response.json();
            fetchEquipment();
        } catch (err) {
            console.error(err.message);
            setError('No se pudo eliminar el equipamiento');
        }
    };

    const filteredEquipment = equipment.filter((item) => {
        return (item.descripcion && item.descripcion.toLowerCase().includes(searchTerm.toLowerCase())) ||
            (item.costo && item.costo.toString().includes(searchTerm)) ||
            (item.id_actividad && item.id_actividad.toString().includes(searchTerm));
    });

    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'descripcion', label: 'Descripción' },
        { key: 'costo', label: 'Costo' },
        { key: 'id_actividad', label: 'ID Actividad' },
    ];

    return (
        <div className="manageEquipment">
            <Button onClick={() => navigate('/control-panel')}>
                Atrás
            </Button>
            <h1 className="manageEquipment-title">Gestionar Equipamiento</h1>
            <div className="manageEquipment-table">
                <div className="manageEquipment-search">
                    <Input
                        placeholder="Buscar equipamiento..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                    />
                    <Button color="#f0ad4e" onClick={() => handleModal(false)}>Agregar</Button>
                </div>
                <Table
                    data={filteredEquipment}
                    columns={columns}
                    onEdit={(equipment) => handleModal(true, equipment)}
                    onDelete={(equipment) => handleDeleteEquipment(equipment.id)}
                />
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={isEditing ? "Editar Equipamiento" : "Agregar Equipamiento"}
            >
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        isEditing ? handleEditEquipment() : handleAddEquipment();
                    }}
                    className="modal-form"
                >
                    {formError && <div className="error-message">{formError}</div>}

                    <div className="form-group">
                        <label>Descripción</label>
                        <Input
                            placeholder="Descripción del equipamiento"
                            value={newEquipmentDescription}
                            onChange={(e) => setNewEquipmentDescription(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>Costo</label>
                        <Input
                            type="number"
                            placeholder="Costo del equipamiento"
                            value={newEquipmentCost}
                            onChange={(e) => setNewEquipmentCost(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>ID Actividad</label>
                        <Input
                            type="number"
                            placeholder="ID de la actividad asociada"
                            value={selectedActivityId}
                            onChange={(e) => setSelectedActivityId(e.target.value)}
                        />
                    </div>

                    <div className="form-actions">
                        <Button type="submit" color="#4CAF50">
                            {isEditing ? 'Actualizar Equipamiento' : 'Crear Equipamiento'}
                        </Button>
                        <Button type="button" color="#f44336" onClick={() => setIsModalOpen(false)}>Cancelar</Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default ManageEquipment;
