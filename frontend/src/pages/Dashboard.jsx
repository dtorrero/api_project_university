import { useState, useEffect } from 'react';
import api from '../config/api';

function Dashboard() {
  const [stats, setStats] = useState({
    users: 0,
    courses: 0,
    subjects: 0,
    documents: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [usersRes, coursesRes, subjectsRes, documentsRes] = await Promise.all([
        api.get('/users'),
        api.get('/courses'),
        api.get('/subjects'),
        api.get('/documents')
      ]);

      setStats({
        users: usersRes.data.length,
        courses: coursesRes.data.length,
        subjects: subjectsRes.data.length,
        documents: documentsRes.data.length
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
      setError('Failed to load dashboard data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { title: 'Total Users', value: stats.users, color: 'bg-blue-500' },
    { title: 'Total Courses', value: stats.courses, color: 'bg-green-500' },
    { title: 'Total Subjects', value: stats.subjects, color: 'bg-purple-500' },
    { title: 'Total Documents', value: stats.documents, color: 'bg-yellow-500' }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">Loading dashboard data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card) => (
          <div
            key={card.title}
            className={`${card.color} rounded-lg shadow-lg p-6 text-white`}
          >
            <h3 className="text-lg font-semibold">{card.title}</h3>
            <p className="text-3xl font-bold mt-2">{card.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h3>
        <p className="text-gray-600">No recent activity to display.</p>
      </div>
    </div>
  );
}

export default Dashboard; 