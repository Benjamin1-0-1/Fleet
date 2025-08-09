import React, { useEffect, useState } from "react";
import { getAll } from "../api/client";

export default function AnalyticsPage() {
  const [overview, setOverview] = useState(null);

  const load = async () => {
    const data = await getAll("/v1/analytics/overview");
    setOverview(data);
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Analytics</h1>
      {!overview ? (
        <div className="bg-white p-4 rounded shadow">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded shadow">
            <div className="text-gray-500">Period (days)</div>
            <div className="text-3xl font-semibold">{overview.period_days}</div>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <div className="text-gray-500">Records</div>
            <div className="text-3xl font-semibold">{overview.records}</div>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <div className="text-gray-500">Total Income</div>
            <div className="text-3xl font-semibold">{overview.total_income}</div>
          </div>
        </div>
      )}
    </div>
  );
}
