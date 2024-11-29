import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Table from '../../components/Table/Table';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import Modal from '../../components/Modal/Modal';
import './ManageInstructors.css';

const ManageInstructors = () => {
    const navigate = useNavigate();

    const [instructors, setInstructors] = useState([]);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newInstructorCi, setNewInstructorCi] = useState(0);
    const [newInstructorName, setNewInstructorName] = useState('');
    const [newInstructorLast_Name, setNewInstructorLast_name] = useState('');
    const [formError, setFormError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedInstructorCi, setSelectedInstructorCi] = useState(0);

    const fetchInstructors = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/instructors/all', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error fetching instructors');
            }

            const data = await response.json();
            setInstructors(data);
        } catch (err) {
            setError(err.message);
            console.error(err);
        }
    };

    useEffect(() => {
        fetchInstructors();
    }, []);

    if (error) {
        return <div>{error}</div>;
    }

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleModal = (isEditingMode = false, instructor = null) => {
        setFormError(null);
        setIsModalOpen(true);
        setIsEditing(isEditingMode);

        if (isEditingMode && instructor) {
            setSelectedInstructorCi(instructor.ci);
            setNewInstructorCi(instructor.ci);
            setNewInstructorName(instructor.nombre || '');
            setNewInstructorLast_name(instructor.apellido || '');
        } else {
            setSelectedInstructorCi(0);
            setNewInstructorCi(0);
            setNewInstructorName('');
            setNewInstructorLast_name('');
        }
    };

    const handleAddInstructor = async () => {
        setFormError(null);

        if (!newInstructorCi || !newInstructorName || !newInstructorLast_Name) {
            setFormError('Todos los campos son requeridos');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5001/api/instructors/add', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ci: newInstructorCi,
                    name: newInstructorName,
                    last_name: newInstructorLast_Name,
                }),
            });

            if (!response.ok) {
                throw new Error('Error al guardar el instructor');
            }

            await response.json();
            setIsModalOpen(false);
            fetchInstructors();
        } catch (err) {
            setFormError(err.message);
            console.error(err);
        }
    };

    const handleEditInstructor = async () => {
        setFormError(null);

        if (!newInstructorName || !newInstructorLast_Name) {
            setFormError('Todos los campos son requeridos');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001/api/instructors/modify/${selectedInstructorCi}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: newInstructorName,
                    last_name: newInstructorLast_Name,
                }),
            });

            if (!response.ok) {
                throw new Error('Error al actualizar el instructor');
            }

            await response.json();
            setIsModalOpen(false);
            fetchInstructors();
        } catch (err) {
            setFormError(err.message);
            console.error(err);
        }
    };

    const handleDeleteInstructor = async (instructorCi) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5001/api/instructors/delete/${instructorCi}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error al eliminar el instructor');
            }

            await response.json();
            fetchInstructors();
        } catch (err) {
            console.error(err.message);
            setError('No se pudo eliminar el instructor');
        }
    };

    const filteredInstructors = instructors.filter((instructor) => {
        return (instructor.ci && instructor.ci.toString().includes(searchTerm.toLowerCase())) ||
            (instructor.nombre && instructor.nombre.toLowerCase().includes(searchTerm.toLowerCase())) ||
            (instructor.apellido && instructor.apellido.toLowerCase().includes(searchTerm.toLowerCase()));
    });

    const columns = [
        { key: 'ci', label: 'CI' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'apellido', label: 'Apellido' },
    ];

    return (
        <div className="manageInstructors">
            <Button onClick={() => navigate('/control-panel')}>
                Atrás
            </Button>
            <h1 className="manageInstructors-title">Gestionar Instructores</h1>
            <div className="manageInstructors-table">
                <div className="manageInstructors-search">
                    <Input
                        placeholder="Buscar instructor..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                    />
                    <Button color="#f0ad4e" onClick={() => handleModal(false)}>Agregar</Button>
                </div>
                <Table
                    data={filteredInstructors}
                    columns={columns}
                    onEdit={(instructor) => handleModal(true, instructor)}
                    onDelete={(instructor) => handleDeleteInstructor(instructor.ci)}
                />
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={isEditing ? "Editar Instructor" : "Agregar Instructor"}
            >
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        isEditing ? handleEditInstructor() : handleAddInstructor();
                    }}
                    className="modal-form"
                >
                    {formError && <div className="error-message">{formError}</div>}

                    {!isEditing && ( // Mostramos el campo CI solo si no está en modo edición.
                        <div className="form-group">
                            <label>CI</label>
                            <Input
                                placeholder="CI del instructor"
                                value={newInstructorCi}
                                onChange={(e) => setNewInstructorCi(e.target.value)}
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label>Nombre</label>
                        <Input
                            placeholder="Nombre del instructor"
                            value={newInstructorName}
                            onChange={(e) => setNewInstructorName(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>Apellido</label>
                        <Input
                            placeholder="Apellido del instructor"
                            value={newInstructorLast_Name}
                            onChange={(e) => setNewInstructorLast_name(e.target.value)}
                        />
                    </div>

                    <div className="form-actions">
                        <Button type="submit" color="#4CAF50">
                            {isEditing ? 'Actualizar Instructor' : 'Crear Instructor'}
                        </Button>
                        <Button type="button" color="#f44336" onClick={() => setIsModalOpen(false)}>Cancelar</Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default ManageInstructors;
