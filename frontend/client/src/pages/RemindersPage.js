import { useEffect, useState } from "react";
import api from "../api/api";
import ReminderList from "../components/ReminderList";
import ReminderForm from "../components/ReminderForm";

export default function RemindersPage() {
  const [items, setItems] = useState([]);
  const refresh = () => api.get("/reminders").then((r) => setItems(r.data));

  useEffect(() => { refresh(); }, []);

  return (
    <section className="page">
      <header className="page__header"><h2>Reminders</h2></header>
      <ReminderForm onSaved={refresh} />
      <ReminderList items={items} onChanged={refresh} />
    </section>
  );
}
