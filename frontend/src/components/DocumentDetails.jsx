import React, { useState, useEffect } from 'react';
import api from '../config/api';

function DocumentDetails({ document, onClose }) {
  const [teacher, setTeacher] = useState(null);
  const [subject, setSubject] = useState(null);
  const [owner, setOwner] = useState(null);

  useEffect(() => {
    const fetchRelatedData = async () => {
      try {
        if (document.teacher_id) {
          const teacherResponse = await api.get(`/users/${document.teacher_id}`);
          setTeacher(teacherResponse.data);
        }
        if (document.subject_id) {
          const subjectResponse = await api.get(`/subjects/id/${document.subject_id}`);
          setSubject(subjectResponse.data);
        }
        if (document.owner) {
          const userResponse = await api.get(`/users/${document.owner}`);
          setOwner(userResponse.data);
        }
      } catch (error) {
        console.error('Error fetching related data:', error);
      }
    };

    fetchRelatedData();
  }, [document]);

  if (!document) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-2xl font-semibold text-gray-800">{document.title}</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <h4 className="text-sm font-medium text-gray-500">Description</h4>
            <p className="mt-1 text-gray-900">{document.description}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium text-gray-500">Type</h4>
              <p className="mt-1 text-gray-900">{document.type}</p>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-500">File URL</h4>
              <a 
                href={document.file_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="mt-1 text-blue-600 hover:text-blue-800"
              >
                View Document
              </a>
            </div>

            {document.grade !== null && (
              <div>
                <h4 className="text-sm font-medium text-gray-500">Grade</h4>
                <p className="mt-1 text-gray-900">{document.grade}</p>
              </div>
            )}

            <div>
              <h4 className="text-sm font-medium text-gray-500">Teacher</h4>
              <p className="mt-1 text-gray-900">
                {teacher ? teacher.name : 'Loading...'}
              </p>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-500">Subject</h4>
              <p className="mt-1 text-gray-900">
                {subject ? subject.name : 'Loading...'}
              </p>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-500">Owner</h4>
              <p className="mt-1 text-gray-900">
                {owner ? owner.name : 'Loading...'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DocumentDetails; 