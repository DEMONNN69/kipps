import { useEffect, useState } from 'react';
import { getReports } from '../api';

export default function Reports() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const data = await getReports();
        setReports(data);
      } catch (err) {
        console.error('Failed to fetch reports');
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <h2 className="text-xl font-semibold mb-4">Reports</h2>
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Reports</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-4 py-2 text-left">ID</th>
              <th className="border border-gray-300 px-4 py-2 text-left">clarity_score</th>
              <th className="border border-gray-300 px-4 py-2 text-left">relevance_score</th>
              <th className="border border-gray-300 px-4 py-2 text-left">accuracy_score</th>
              <th className="border border-gray-300 px-4 py-2 text-left">completeness_score</th>
              <th className="border border-gray-300 px-4 py-2 text-left">sentiment</th>
              <th className="border border-gray-300 px-4 py-2 text-left">empathy_score</th>
              <th className="border border-gray-300 px-4 py-2 text-left">avg_response_time</th>
              <th className="border border-gray-300 px-4 py-2 text-left">resolved</th>
              <th className="border border-gray-300 px-4 py-2 text-left">escalation_needed</th>
              <th className="border border-gray-300 px-4 py-2 text-left">fallback_count</th>
              <th className="border border-gray-300 px-4 py-2 text-left">overall_score</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => (
              <tr key={report.id}>
                <td className="border border-gray-300 px-4 py-2">{report.id}</td>
                <td className="border border-gray-300 px-4 py-2">{report.clarity_score}</td>
                <td className="border border-gray-300 px-4 py-2">{report.relevance_score}</td>
                <td className="border border-gray-300 px-4 py-2">{report.accuracy_score}</td>
                <td className="border border-gray-300 px-4 py-2">{report.completeness_score}</td>
                <td className="border border-gray-300 px-4 py-2">{report.sentiment}</td>
                <td className="border border-gray-300 px-4 py-2">{report.empathy_score}</td>
                <td className="border border-gray-300 px-4 py-2">{report.avg_response_time}</td>
                <td className="border border-gray-300 px-4 py-2">{report.resolved ? 'true' : 'false'}</td>
                <td className="border border-gray-300 px-4 py-2">{report.escalation_needed ? 'true' : 'false'}</td>
                <td className="border border-gray-300 px-4 py-2">{report.fallback_count}</td>
                <td className="border border-gray-300 px-4 py-2">{report.overall_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

