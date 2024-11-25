import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Table from '../../components/Table/Table';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import Modal from '../../components/Modal/Modal';
import './ManageClasses.css';

const ManageClasses = () => {
    const navigate = useNavigate();

    const [classes, setClasses] = useState([]);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formError, setFormError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedClass, setSelectedClass] = useState(null);

    const [formData, setFormData] = useState({
        ci_instructor: '',
        id_actividad: '',
        id_turno: '',
        dictada: false,
    });

    const fetchClasses = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/classes/all', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorHtml = await response.text();
                console.error('Error response HTML:', errorHtml);
                throw new Error('Error fetching classes');
            }

            const data = await response.json();
            setClasses(data);
        } catch (err) {
            setError(err.message);
            console.error(err);
        }
    };

    useEffect(() => {
        fetchClasses();
    }, []);

    const handleModal = (isEditingMode = false, classData = null) => {
        setFormError(null);
        setIsModalOpen(true);
        setIsEditing(isEditingMode);

        if (isEditingMode && classData) {
            setSelectedClass(classData);
            setFormData({
                ci_instructor: classData.ci_instructor || '',
                id_actividad: classData.id_actividad || '',
                id_turno: classData.id_turno || '',
                dictada: !!classData.dictada, // Convertir a booleano
            });
        } else {
            setSelectedClass(null);
            setFormData({
                ci_instructor: '',
                id_actividad: '',
                id_turno: '',
                dictada: false,
            });
        }
    };

    const handleAddOrEditClass = async () => {
        const url = isEditing
            ? `http://localhost:5001/api/classes/${selectedClass.id}`
            : 'http://localhost:5001/api/classes';

        const method = isEditing ? 'PUT' : 'POST';

        // Validación previa
        if (!formData.ci_instructor || !formData.id_actividad || !formData.id_turno) {
            setFormError('Todos los campos son requeridos');
            return;
        }

        // Ajustar nombres y tipos de datos
        const adjustedData = {
            ci_instructor: parseInt(formData.ci_instructor, 10), // Asegura que sea entero
            id_activity: parseInt(formData.id_actividad, 10),   // Cambia el nombre y asegura que sea entero
            id_shift: parseInt(formData.id_turno, 10),          // Cambia el nombre y asegura que sea entero
            dictated: Boolean(formData.dictada),                // Cambia el nombre y asegura que sea booleano
        };

        console.log('Datos enviados al backend:', adjustedData);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(url, {
                method,
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(adjustedData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error saving class');
            }

            await response.json();
            setIsModalOpen(false);
            fetchClasses();
        } catch (err) {
            setFormError(err.message);
            console.error(err);
        }
    };

    const handleDeleteClass = async (classId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001/api/classes/${classId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error deleting class');
            }

            await response.json();
            fetchClasses();
        } catch (err) {
            console.error(err.message);
            setError('No se pudo eliminar la clase');
        }
    };

    const filteredClasses = classes.filter((classData) => {
        return (
            (classData.id && classData.id.toString().includes(searchTerm)) ||
            (classData.ci_instructor &&
                classData.ci_instructor.toString().includes(searchTerm))
        );
    });

    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'ci_instructor', label: 'Instructor CI' },
        { key: 'id_actividad', label: 'Actividad' }, // Muestra el ID de la actividad
        { key: 'id_turno', label: 'Turno' }, // Muestra el ID del turno
        {
            key: 'dictada',
            label: 'Dictado',
            render: (value) => (value ? 'Sí' : 'No'), // Renderiza 0 como "No" y 1 como "Sí"
        },
    ];

    return (
        <div className="manageClasses">
            <Button onClick={() => navigate('/control-panel')}>
                Atrás
            </Button>
            <h1 className="manageClasses-title">Gestionar Clases</h1>
            <div className="manageClasses-table">
                <div className="manageClasses-search">
                    <Input
                        placeholder="Buscar clase..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <Button color="#f0ad4e" onClick={() => handleModal(false)}>Agregar</Button>
                </div>
                <Table
                    data={filteredClasses}
                    columns={columns}
                    onEdit={(classData) => handleModal(true, classData)}
                    onDelete={(classData) => handleDeleteClass(classData.id)}
                />
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={isEditing ? 'Editar Clase' : 'Agregar Clase'}
            >
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        handleAddOrEditClass();
                    }}
                    className="modal-form"
                >
                    {formError && <div className="error-message">{formError}</div>}

                    <div className="form-group">
                        <label>CI Instructor</label>
                        <Input
                            value={formData.ci_instructor}
                            onChange={(e) =>
                                setFormData({ ...formData, ci_instructor: e.target.value })
                            }
                        />
                    </div>

                    <div className="form-group">
                        <label>ID Actividad</label>
                        <Input
                            value={formData.id_actividad}
                            onChange={(e) =>
                                setFormData({ ...formData, id_actividad: e.target.value })
                            }
                        />
                    </div>

                    <div className="form-group">
                        <label>ID Turno</label>
                        <Input
                            value={formData.id_turno}
                            onChange={(e) =>
                                setFormData({ ...formData, id_turno: e.target.value })
                            }
                        />
                    </div>

                    <div className="form-group">
                        <label>Dictado</label>
                        <Input
                            type="checkbox"
                            checked={formData.dictada}
                            onChange={(e) =>
                                setFormData({ ...formData, dictada: e.target.checked })
                            }
                        />
                    </div>

                    <div className="form-actions">
                        <Button type="submit" color="#4CAF50">
                            {isEditing ? 'Actualizar Clase' : 'Crear Clase'}
                        </Button>
                        <Button type="button" color="#f44336" onClick={() => setIsModalOpen(false)}>
                            Cancelar
                        </Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default ManageClasses;
