import { useState, useEffect } from 'react';
import api from '../config/api';
import Table from '../components/Table';

function Subjects() {
  const [subjects, setSubjects] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    teacher_id: null
  });

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'description', label: 'Description' },
    { 
      key: 'teacher_id', 
      label: 'Teacher',
      render: (teacherId) => {
        const teacher = teachers.find(t => t.id === teacherId);
        return teacher ? teacher.name : 'Not assigned';
      }
    }
  ];

  useEffect(() => {
    fetchSubjects();
    fetchTeachers();
  }, []);

  const fetchSubjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/subjects');
      setSubjects(response.data);
    } catch (error) {
      console.error('Error fetching subjects:', error);
      setError('Failed to load subjects. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const fetchTeachers = async () => {
    try {
      const response = await api.get('/users');
      const teacherUsers = response.data.filter(user => user.type === 'teacher');
      setTeachers(teacherUsers);
    } catch (error) {
      console.error('Error fetching teachers:', error);
    }
  };

  const handleViewSubject = (subject) => {
    setSelectedSubject(subject);
    setIsViewModalOpen(true);
  };

  const handleEdit = (subject) => {
    setSelectedSubject(subject);
    setFormData({
      name: subject.name,
      description: subject.description,
      teacher_id: subject.teacher_id
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (subject) => {
    if (window.confirm('Are you sure you want to delete this subject?')) {
      try {
        await api.delete(`/subjects/${subject.id}`);
        fetchSubjects();
      } catch (error) {
        console.error('Error deleting subject:', error);
        alert('Failed to delete subject. Please try again.');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        teacher_id: formData.teacher_id ? parseInt(formData.teacher_id) : null
      };

      if (selectedSubject) {
        await api.put(`/subjects/${selectedSubject.id}`, submitData);
      } else {
        await api.post('/subjects', submitData);
      }
      setIsModalOpen(false);
      setSelectedSubject(null);
      setFormData({ name: '', description: '', teacher_id: null });
      fetchSubjects();
    } catch (error) {
      console.error('Error saving subject:', error);
      alert('Failed to save subject. Please try again.');
    }
  };

  const getTeacherById = (teacherId) => {
    return teachers.find(teacher => teacher.id === teacherId);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">Loading subjects...</div>
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
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Subjects</h2>
        <button
          onClick={() => {
            setSelectedSubject(null);
            setFormData({ name: '', description: '', teacher_id: null });
            setIsModalOpen(true);
          }}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Add Subject
        </button>
      </div>

      <Table
        columns={columns}
        data={subjects}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onRowClick={handleViewSubject}
      />

      {/* Edit/Add Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-xl font-semibold mb-4">
              {selectedSubject ? 'Edit Subject' : 'Add Subject'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  required
                  minLength={1}
                  maxLength={100}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  rows="3"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Teacher</label>
                <select
                  value={formData.teacher_id || ''}
                  onChange={(e) => setFormData({ ...formData, teacher_id: e.target.value ? parseInt(e.target.value) : null })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="">Select a teacher</option>
                  {teachers.map((teacher) => (
                    <option key={teacher.id} value={teacher.id}>
                      {teacher.name} ({teacher.email})
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-gray-700 hover:text-gray-900"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  {selectedSubject ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* View Modal */}
      {isViewModalOpen && selectedSubject && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-semibold">Subject Details</h3>
              <button
                onClick={() => setIsViewModalOpen(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-6">
              <div>
                <h4 className="text-lg font-medium text-gray-900 mb-2">{selectedSubject.name}</h4>
                <p className="text-sm text-gray-500">Subject ID: {selectedSubject.id}</p>
              </div>

              <div>
                <h4 className="text-lg font-medium text-gray-900 mb-2">Description</h4>
                <p className="text-gray-600">{selectedSubject.description}</p>
              </div>

              <div>
                <h4 className="text-lg font-medium text-gray-900 mb-2">Assigned Teacher</h4>
                {selectedSubject.teacher_id ? (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    {(() => {
                      const teacher = getTeacherById(selectedSubject.teacher_id);
                      return teacher ? (
                        <>
                          <h5 className="font-medium text-gray-900">{teacher.name}</h5>
                          <p className="text-sm text-gray-600 mt-1">{teacher.email}</p>
                        </>
                      ) : (
                        <p className="text-gray-600">Teacher not found</p>
                      );
                    })()}
                  </div>
                ) : (
                  <p className="text-gray-600">No teacher assigned</p>
                )}
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setIsViewModalOpen(false)}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Subjects; 