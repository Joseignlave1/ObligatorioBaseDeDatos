import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Table from "../../components/Table/Table";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";
import Modal from "../../components/Modal/Modal";
import "./ManageStudents.css";

const ManageStudents = () => {
    const navigate = useNavigate();

    const [students, setStudents] = useState([]);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newStudentSurname, setNewStudentSurname] = useState("");
    const [newStudentCi, setNewStudentCi] = useState(0);
    const [newStudentEmail, setNewStudentEmail] = useState("");
    const [newStudentBornDate, setNewStudentBornDate] = useState("");
    const [newStudentName, setNewStudentName] = useState("");
    const [newStudentPhone, setNewStudentPhone] = useState("");
    const [formError, setFormError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedStudentCi, setSelectedStudentCi] = useState(0);



    const getAllStudents = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5001/api/students/all", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Error fetching students");
        }

        const data = await response.json();
        setStudents(data);
      } catch (error) {
        setError(error.message);
        console.log(error);
      }
    };

    useEffect(() => {
        getAllStudents();
    }, [])
    
    if(error) {
      return <div>{error}</div>;
    }

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleModal = (isEditingMode = false, student = null) => {
        setFormError(null);
        setIsModalOpen(true);
        setIsEditing(isEditingMode);

        if (isEditingMode && student) {
            setSelectedStudentCi(student.ci);
            setNewStudentCi(student.ci);
            setNewStudentSurname(student.apellido || '');
            setNewStudentEmail(student.correo || '');
            setNewStudentBornDate(student.fecha_nacimiento || '')
            setNewStudentPhone(student.telefono || '');
            setNewStudentName(student.nombre || '');
        } else {
             setSelectedStudentCi(0);
             setNewStudentCi(0);
             setNewStudentSurname('');
             setNewStudentEmail('');
             setNewStudentBornDate('');
             setNewStudentPhone('');
             setNewStudentName('');
        }
    };

    const handleAddStudents = async () => {
      setFormError(null);

      if (
        !newStudentSurname ||
        !newStudentCi ||
        !newStudentEmail ||
        !newStudentBornDate ||
        !newStudentName ||
        !newStudentPhone
      ) {
        setFormError("Todos los campos son requeridos");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5001/api/students", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ci: newStudentCi,
            first_name: newStudentName,
            last_name: newStudentSurname,
            birth_date: newStudentBornDate,
            contact_phone: newStudentPhone,
            email_address: newStudentEmail,
          }),
        });

        if (!response.ok) {
          throw new Error("Error al guardar la actividad");
        }

        await response.json();
        setIsModalOpen(false);
        await getAllStudents();
      } catch (err) {
        setFormError(err.message);
        console.error(err);
      }
    };

    
    const handleEditStudent = async () => {
    setFormError(null); 

    try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `http://localhost:5001/api/students/${selectedStudentCi}`,
          {
            method: "PUT",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              first_name: newStudentName,
              last_name: newStudentSurname,
              birth_date: newStudentBornDate,
              contact_phone: newStudentPhone,
              email_address: newStudentEmail,
            }),
          }
        );

        if (!response.ok) {
        throw new Error("Error al actualizar el estudiante");
        }

        await response.json();
        setIsModalOpen(false);
        await getAllStudents();
    } catch (err) {
        setFormError(err.message);
        console.error(err);
    }
    };

    const handleDeleteActivity = async (studentCi) => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `http://localhost:5001/api/students/${studentCi}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error("Error al eliminar la actividad");
        }

        await response.json();
        await getAllStudents();
      } catch (err) {
        console.error(err.message);
        setError("No se pudo eliminar la actividad");
      }
    };
    
    const filteredStudents = students.filter((student) => {
            return  (student.apellido && student.apellido.toLowerCase().includes(searchTerm.toLowerCase())) ||
                    (student.ci && student.ci.toString().includes(searchTerm.toLocaleLowerCase())) ||
                    (student.correo && student.correo.toLowerCase().includes(searchTerm.toLocaleLowerCase())) ||
                    (student.fecha_nacimiento && student.fecha_nacimiento.toLowerCase().includes(searchTerm.toLocaleLowerCase())) ||
                    (student.nombre && student.nombre.toLowerCase().includes(searchTerm.toLocaleLowerCase())) ||
                    (student.telefono && student.telefono.toLowerCase().includes(searchTerm.toLocaleLowerCase()));
        });

         const columns = [
        { key: 'ci', label: 'CI' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'apellido', label: 'Apellido' },
        { key: 'fecha_nacimiento', label: 'Fecha De Nacimiento' },
        { key: 'correo', label: 'Correo' },
        { key: 'telefono', label: 'Telefono'}
    ];

    return (
        <div className="manageActivities">
            <Button onClick={() => navigate('/control-panel')}>
                Atrás
            </Button>
            <h1 className="manageActivities-title">Gestionar Alumnos</h1>
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
                    data={filteredStudents}
                    columns={columns}
                    onEdit={(student) => handleModal(true, student)}
                    onDelete={(student) => handleDeleteActivity(student.ci)}
                />
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={isEditing ? "Editar Estudiante" : "Agregar Estudiante"}
            >
                <form
          onSubmit={(e) => {
              e.preventDefault();
              isEditing ? handleEditStudent() : handleAddStudents();
          }}
          className="modal-form"
      >
      {formError && <div className="error-message">{formError}</div>}

      {!isEditing && ( // Mostramos el campo CI solo si no está en modo edición.
          <div className="form-group">
              <label>CI</label>
              <Input 
                  type="number"
                  placeholder="CI del Estudiante"
                  value={newStudentCi}
                  onChange={(e) => setNewStudentCi(e.target.value)}
              />
          </div>
      )}

            <div className="form-group">
                <label>Nombre</label>
                <Input 
                    placeholder="Nombre Del Estudiante"
                    value={newStudentName}
                    onChange={(e) => setNewStudentName(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label>Apellido</label>
                <Input 
                    placeholder="Apellido Del Estudiante"
                    value={newStudentSurname}
                    onChange={(e) => setNewStudentSurname(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label>Fecha De Nacimiento</label>
                <Input 
                    type="date"
                    placeholder="Fecha De Nacimiento Del Estudiante"
                    value={newStudentBornDate}
                    onChange={(e) => setNewStudentBornDate(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label>Correo</label>
                <Input 
                    placeholder="Correo Del Estudiante"
                    value={newStudentEmail}
                    onChange={(e) => setNewStudentEmail(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label>Teléfono</label>
                <Input 
                    placeholder="Teléfono Del Estudiante"
                    value={newStudentPhone}
                    onChange={(e) => setNewStudentPhone(e.target.value)}
                />
            </div>

            <div className="form-actions">
                <Button type="submit" color="#4CAF50">
                    {isEditing ? 'Actualizar Estudiante' : 'Crear Estudiante'}
                </Button>
                <Button type="button" color="#f44336" onClick={() => setIsModalOpen(false)}>Cancelar</Button>
            </div>
        </form>

            </Modal>
        </div>
    );
}
export default ManageStudents;