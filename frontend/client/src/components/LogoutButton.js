export default function LogoutButton() {
  const logout = () => { localStorage.removeItem("vm_token"); window.location.href = "/"; };
  return <button className="btn-outline" onClick={logout}>Logout</button>;
}
