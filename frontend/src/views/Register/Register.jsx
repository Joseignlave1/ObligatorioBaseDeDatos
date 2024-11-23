import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Importar useNavigate
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import './Register.css';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate(); // Crear la constante para el hook

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://localhost:5001/api/register", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                alert('Registration successful');
                console.log('Token:', data.token);
                navigate('/login'); // Redirigir al login después del registro exitoso
            } else {
                alert(data.message || 'Error during registration');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong');
        }
    };

    return (
        <div className="auth-page"> {/* Centra la tarjeta en la pantalla */}
            <div className="auth-container"> {/* Define el diseño de la tarjeta */}
                <h1 className="auth-title">Register</h1> {/* Título estilizado */}
                <form className="auth-form" onSubmit={handleSubmit}>
                    {/* Campo de entrada para el email */}
                    <div className="auth-form-group">
                        <Input
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            type="email"
                        />
                    </div>
                    {/* Campo de entrada para la contraseña */}
                    <div className="auth-form-group">
                        <Input
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            type="password"
                        />
                    </div>
                    {/* Botón para enviar el formulario */}
                    <div className="auth-button">
                        <Button>Register</Button>
                    </div>
                </form>
                {/* Enlace a la página de login */}
                <a href="/login" className="auth-link">
                    Already have an account? Login here
                </a>
            </div>
        </div>
    );
};

export default Register;
