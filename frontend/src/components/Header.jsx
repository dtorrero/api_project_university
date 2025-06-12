import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  UserGroupIcon,
  AcademicCapIcon,
  BookOpenIcon,
  DocumentIcon
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Users', href: '/users', icon: UserGroupIcon },
  { name: 'Courses', href: '/courses', icon: AcademicCapIcon },
  { name: 'Subjects', href: '/subjects', icon: BookOpenIcon },
  { name: 'Documents', href: '/documents', icon: DocumentIcon },
];

function Header() {
  const location = useLocation();

  return (
    <header className="w-4/5 h-[20vh] mx-auto bg-white shadow-lg rounded-b-3xl">
      <div className="h-full flex flex-col justify-between p-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-800">School Management System</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">Welcome, Admin</span>
          </div>
        </div>
        
        <nav className="flex space-x-8">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-200 ${
                  isActive
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <item.icon className="h-5 w-5" />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}

export default Header; 