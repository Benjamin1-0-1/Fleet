import { Routes, Route } from "react-router-dom";
import VehicleList from "../components/VehicleList";
import VehicleForm from "../components/VehicleForm";

export default function VehiclesPage() {
  return (
    <Routes>
      <Route path="/" element={<VehicleList />} />
      <Route path="new" element={<VehicleForm />} />
      <Route path=":id/edit" element={<VehicleForm />} />
    </Routes>
  );
}
