import { useState, useEffect } from 'react';
import api from '../config/api';
import Table from '../components/Table';

function Courses() {
  const [courses, setCourses] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [isAddSubjectModalOpen, setIsAddSubjectModalOpen] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    subjects: []
  });

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { 
      key: 'subjects', 
      label: 'Subjects',
      render: (subjects, course) => (
        <button
          onClick={() => handleViewCourse(course)}
          className="text-blue-500 hover:text-blue-700"
        >
          View Subjects ({subjects.length})
        </button>
      )
    }
  ];

  useEffect(() => {
    fetchCourses();
    fetchSubjects();
  }, []);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/courses');
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
      setError('Failed to load courses. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const fetchSubjects = async () => {
    try {
      const response = await api.get('/subjects');
      setSubjects(response.data);
    } catch (error) {
      console.error('Error fetching subjects:', error);
    }
  };

  const handleViewCourse = (course) => {
    setSelectedCourse(course);
    setIsViewModalOpen(true);
  };

  const handleEdit = (course) => {
    setSelectedCourse(course);
    setFormData({
      name: course.name,
      subjects: course.subjects || []
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (course) => {
    if (window.confirm('Are you sure you want to delete this course?')) {
      try {
        await api.delete(`/courses/${course.id}`);
        fetchCourses();
      } catch (error) {
        console.error('Error deleting course:', error);
        alert('Failed to delete course. Please try again.');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedCourse) {
        await api.put(`/courses/${selectedCourse.id}`, formData);
      } else {
        await api.post('/courses', formData);
      }
      setIsModalOpen(false);
      setSelectedCourse(null);
      setFormData({ name: '', subjects: [] });
      fetchCourses();
    } catch (error) {
      console.error('Error saving course:', error);
      alert('Failed to save course. Please try again.');
    }
  };

  const handleRemoveSubject = (subjectId) => {
    setFormData(prev => ({
      ...prev,
      subjects: prev.subjects.filter(id => id !== subjectId)
    }));
  };

  const handleAddSubject = (subjectId) => {
    if (formData.subjects.length >= 4) {
      alert('A course can have a maximum of 4 subjects.');
      return;
    }
    setFormData(prev => ({
      ...prev,
      subjects: [...prev.subjects, subjectId]
    }));
    setIsAddSubjectModalOpen(false);
  };

  const getAvailableSubjects = () => {
    return subjects.filter(subject => !formData.subjects.includes(subject.id));
  };

  const getSubjectById = (subjectId) => {
    return subjects.find(subject => subject.id === subjectId);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">Loading courses...</div>
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
        <h2 className="text-2xl font-bold text-gray-800">Courses</h2>
        <button
          onClick={() => {
            setSelectedCourse(null);
            setFormData({ name: '', subjects: [] });
            setIsModalOpen(true);
          }}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Add Course
        </button>
      </div>

      <Table
        columns={columns}
        data={courses}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      {/* Edit/Add Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
            <h3 className="text-xl font-semibold mb-4">
              {selectedCourse ? 'Edit Course' : 'Add Course'}
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
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium text-gray-700">Subjects</label>
                  {formData.subjects.length < 4 && (
                    <button
                      type="button"
                      onClick={() => setIsAddSubjectModalOpen(true)}
                      className="text-blue-500 hover:text-blue-700 flex items-center"
                    >
                      <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                      </svg>
                      Add Subject
                    </button>
                  )}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {formData.subjects.map((subjectId) => {
                    const subject = getSubjectById(subjectId);
                    return subject ? (
                      <div key={subject.id} className="bg-gray-50 p-4 rounded-lg flex justify-between items-start">
                        <div>
                          <h5 className="font-medium text-gray-900">{subject.name}</h5>
                          <p className="text-sm text-gray-600 mt-1">{subject.description}</p>
                        </div>
                        <button
                          type="button"
                          onClick={() => handleRemoveSubject(subject.id)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </div>
                    ) : null;
                  })}
                </div>
                {formData.subjects.length === 0 && (
                  <p className="text-sm text-gray-500 mt-2">No subjects added yet. Click the "Add Subject" button to add subjects.</p>
                )}
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
                  {selectedCourse ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Subject Modal */}
      {isAddSubjectModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-semibold">Add Subject</h3>
              <button
                onClick={() => setIsAddSubjectModalOpen(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-4">
              {getAvailableSubjects().map((subject) => (
                <div
                  key={subject.id}
                  className="bg-gray-50 p-4 rounded-lg cursor-pointer hover:bg-gray-100"
                  onClick={() => handleAddSubject(subject.id)}
                >
                  <h5 className="font-medium text-gray-900">{subject.name}</h5>
                  <p className="text-sm text-gray-600 mt-1">{subject.description}</p>
                </div>
              ))}
              {getAvailableSubjects().length === 0 && (
                <p className="text-sm text-gray-500">No available subjects to add.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* View Modal */}
      {isViewModalOpen && selectedCourse && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-semibold">Course Details</h3>
              <button
                onClick={() => setIsViewModalOpen(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="mb-6">
              <h4 className="text-lg font-medium text-gray-900 mb-2">{selectedCourse.name}</h4>
              <p className="text-sm text-gray-500">Course ID: {selectedCourse.id}</p>
            </div>

            <div>
              <h4 className="text-lg font-medium text-gray-900 mb-4">Assigned Subjects</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {selectedCourse.subjects.map((subjectId) => {
                  const subject = getSubjectById(subjectId);
                  return subject ? (
                    <div key={subject.id} className="bg-gray-50 p-4 rounded-lg">
                      <h5 className="font-medium text-gray-900">{subject.name}</h5>
                      <p className="text-sm text-gray-600 mt-1">{subject.description}</p>
                      <p className="text-xs text-gray-500 mt-2">Subject ID: {subject.id}</p>
                    </div>
                  ) : null;
                })}
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

export default Courses; 