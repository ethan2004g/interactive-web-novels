'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuthContext } from '@/contexts';

interface NavItem {
  name: string;
  href: string;
  icon: string;
  authorOnly?: boolean;
  readerOnly?: boolean;
}

const navItems: NavItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: '📊',
  },
  {
    name: 'My Books',
    href: '/dashboard/books',
    icon: '📚',
    authorOnly: true,
  },
  {
    name: 'Create Book',
    href: '/dashboard/books/new',
    icon: '➕',
    authorOnly: true,
  },
  {
    name: 'My Library',
    href: '/dashboard/library',
    icon: '📖',
    readerOnly: true,
  },
  {
    name: 'Reading Progress',
    href: '/dashboard/progress',
    icon: '📈',
    readerOnly: true,
  },
  {
    name: 'Bookmarks',
    href: '/dashboard/bookmarks',
    icon: '🔖',
  },
  {
    name: 'Statistics',
    href: '/dashboard/stats',
    icon: '📊',
    authorOnly: true,
  },
  {
    name: 'Templates',
    href: '/dashboard/templates',
    icon: '🎨',
    authorOnly: true,
  },
  {
    name: 'Settings',
    href: '/dashboard/settings',
    icon: '⚙️',
  },
];

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export function Sidebar({ isOpen = true, onClose }: SidebarProps) {
  const pathname = usePathname();
  const { user, isAuthor } = useAuthContext();

  const filteredNavItems = navItems.filter((item) => {
    if (item.authorOnly && !isAuthor) return false;
    if (item.readerOnly && isAuthor) return false;
    return true;
  });

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && onClose && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transform transition-transform duration-200 ease-in-out lg:transform-none ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <nav className="mt-6 px-3">
          <div className="space-y-1">
          {filteredNavItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <span className="text-xl mr-3">{item.icon}</span>
                {item.name}
              </Link>
            );
          })}
        </div>

        {/* User info section */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="px-3 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Account
          </div>
          <div className="px-3 py-2">
            <div className="flex items-center">
              <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-medium">
                {user?.username.charAt(0).toUpperCase()}
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-900">
                  {user?.username}
                </p>
                <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </aside>
    </>
  );
}

