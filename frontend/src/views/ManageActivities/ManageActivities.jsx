import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Table from '../../components/Table/Table';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import Modal from '../../components/Modal/Modal'; 
import './ManageActivities.css';

const ManageActivities = () => {
    const navigate = useNavigate();

    const [activities, setActivities] = useState([]); 
    const [error, setError] = useState(null); 
    const [searchTerm, setSearchTerm] = useState(''); 
    const [isModalOpen, setIsModalOpen] = useState(false); 
    const [newActivityDescription, setNewActivityDescription] = useState('');
    const [newActivityCost, setNewActivityCost] = useState('');
    const [newActivityMinAge, setNewActivityMinAge] = useState('');
    const [formError, setFormError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedActivityId, setSelectedActivityId] = useState(null);

    const fetchActivities = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/activities/all', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error fetching activities');
            }

            const data = await response.json();
            setActivities(data);
        } catch (err) {
            setError(err.message);
            console.error(err);
        }
    };

    useEffect(() => {
        fetchActivities();
    }, []);

    if (error) {
        return <div>{error}</div>;
    }

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleModal = (isEditingMode = false, activity = null) => {
        setFormError(null);
        setIsModalOpen(true);
        setIsEditing(isEditingMode);

        if (isEditingMode && activity) {
            setSelectedActivityId(activity.id);
            setNewActivityDescription(activity.descripcion || '');
            setNewActivityCost(activity.costo || '');
            setNewActivityMinAge(activity.edad_minima || '');
        } else {
            setSelectedActivityId(null);
            setNewActivityDescription('');
            setNewActivityCost('');
            setNewActivityMinAge('');
        }
    };

const handleAddActivity = async () => {
    setFormError(null);

    if (!newActivityDescription || !newActivityCost || !newActivityMinAge) {
        setFormError('Todos los campos son requeridos');
        return;
    }

    try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:5001/api/activities', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                description: newActivityDescription,
                cost: parseFloat(newActivityCost),
                minimumAge: parseInt(newActivityMinAge),
            }),
        });

        if (!response.ok) {
            throw new Error('Error al guardar la actividad');
        }

        await response.json(); 
        setIsModalOpen(false);
        fetchActivities(); 
    } catch (err) {
        setFormError(err.message);
        console.error(err);
    }
};

const handleEditActivity = async () => {
    setFormError(null);

    if (!newActivityDescription || !newActivityCost || !newActivityMinAge) {
        setFormError('Todos los campos son requeridos');
        return;
    }

    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:5001/api/activities/${selectedActivityId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                description: newActivityDescription,
                cost: parseFloat(newActivityCost),
                minimumAge: parseInt(newActivityMinAge),
            }),
        });

        if (!response.ok) {
            throw new Error('Error al actualizar la actividad');
        }

        await response.json(); 
        setIsModalOpen(false); 
        fetchActivities(); 
    } catch (err) {
        setFormError(err.message);
        console.error(err);
    }
};

const handleDeleteActivity = async (activityId) => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:5001/api/activities/${activityId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Error al eliminar la actividad');
        }

        await response.json(); 
        fetchActivities(); 
    } catch (err) {
        console.error(err.message);
        setError('No se pudo eliminar la actividad');
    }
};

    const filteredActivities = activities.filter((activity) => {
        return  (activity.descripcion && activity.descripcion.toLowerCase().includes(searchTerm.toLowerCase())) ||
                (activity.costo && activity.costo.toString().includes(searchTerm)) ||
                (activity.edad_minima && activity.edad_minima.toString().includes(searchTerm));
    });

    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'descripcion', label: 'Descripción' },
        { key: 'costo', label: 'Costo' },
        { key: 'edad_minima', label: 'Edad Mínima' },
    ];

    return (
        <div className="manageActivities">
            <Button onClick={() => navigate('/control-panel')}>
                Atrás
            </Button>
            <h1 className="manageActivities-title">Gestionar Actividades</h1>
            <div className="manageActivities-table">
                <div className="manageActivities-search">
                    <Input
                        placeholder="Buscar actividad..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                    />
                    <Button  color="#f0ad4e" onClick={() => handleModal(false)}>Agregar</Button>
                </div>
                <Table
                    data={filteredActivities}
                    columns={columns}
                    onEdit={(activity) => handleModal(true, activity)}
                    onDelete={(activity) => handleDeleteActivity(activity.id)}
                />
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={isEditing ? "Editar Actividad" : "Agregar Actividad"}
            >
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        isEditing ? handleEditActivity() : handleAddActivity();
                    }}
                    className="modal-form"
                >
                    {formError && <div className="error-message">{formError}</div>}

                    <div className="form-group">
                        <label>Descripción</label>
                        <Input 
                            placeholder="Descripción de la actividad" 
                            value={newActivityDescription}
                            onChange={(e) => setNewActivityDescription(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>Costo</label>
                        <Input 
                            type="number" 
                            placeholder="Costo de la actividad"
                            value={newActivityCost}
                            onChange={(e) => setNewActivityCost(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>Edad Mínima</label>
                        <Input 
                            type="number" 
                            placeholder="Edad mínima para la actividad"
                            value={newActivityMinAge}
                            onChange={(e) => setNewActivityMinAge(e.target.value)}
                        />
                    </div>

                    <div className="form-actions">
                        <Button type="submit" color="#4CAF50">
                            {isEditing ? 'Actualizar Actividad' : 'Crear Actividad'}
                        </Button>
                        <Button type="button" color="#f44336" onClick={() => setIsModalOpen(false)}>Cancelar</Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default ManageActivities;
