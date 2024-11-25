import React from "react";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Register from "./views/Register/Register";
import Login from './views/Login/Login';
import ControlPanel from './views/ControlPanel/ControlPanel';
import ManageActivities from './views/ManageActivities/ManageActivities';
import ManageClasses from "./views/ManageClasses/ManageClasses";
// import ManageInstructors from './views/ManageInstructors/ManageInstructors';
import ManageShifts from './views/ManageShifts/ManageShifts';
import ManageStudents from './views/ManageStudents/ManageStudents';
import Reports from './views/Reports/Reports';

import './App.css';

const App = () => {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/control-panel" element={<ControlPanel />} />
        <Route path="/manage-activities" element={<ManageActivities />} />
        <Route path="/manage-classes" element={<ManageClasses />} />
        {/* <Route path="/manage-instructors" element={<ManageInstructors />} />*/}
        <Route path="/manage-shifts" element={<ManageShifts />} />
        <Route path="/manage-students" element={<ManageStudents />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
