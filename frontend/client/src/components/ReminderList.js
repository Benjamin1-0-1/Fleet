import api from "../api/api";

export default function ReminderList({ items, onChanged }) {
  const markSent = async (id) => {
    try {
      await api.patch(`/reminders/${id}`, { sent: true });
      onChanged?.();
    } catch (err) {
      console.error("[ReminderList] markSent failed:", err);
      alert("Failed to mark as sent.");
    }
  };

  const remove = async (id) => {
    if (!window.confirm("Delete reminder?")) return;
    try {
      await api.delete(`/reminders/${id}`);
      onChanged?.();
    } catch (err) {
      console.error("[ReminderList] delete failed:", err);
      alert("Failed to delete reminder.");
    }
  };

  return (
    <ul className="cards">
      {items.map((r) => (
        <li key={r.id} className="card">
          <div>
            <strong>{r.reminder_type}</strong> — Vehicle #{r.vehicle_id}
            <div className="sub">Due: {r.due_date}</div>
          </div>
          <div className="card__actions">
            {!r.sent && <button onClick={() => markSent(r.id)}>Mark Sent</button>}
            <button className="danger" onClick={() => remove(r.id)}>Delete</button>
          </div>
        </li>
      ))}
    </ul>
  );
}
