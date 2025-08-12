import { Routes, Route } from "react-router-dom";
import ClientList from "../components/ClientList";
import ClientForm from "../components/ClientForm";

export default function ClientsPage() {
  return (
    <Routes>
      <Route path="/" element={<ClientList />} />
      <Route path="new" element={<ClientForm />} />
      <Route path=":id/edit" element={<ClientForm />} />
    </Routes>
  );
}
