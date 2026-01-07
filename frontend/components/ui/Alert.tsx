import { ReactNode } from 'react';

interface AlertProps {
  variant?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  children: ReactNode;
  className?: string;
}

export function Alert({ variant = 'info', title, children, className = '' }: AlertProps) {
  const variantStyles = {
    info: {
      container: 'bg-blue-50 border-blue-200 text-blue-800',
      icon: 'ℹ️',
      titleColor: 'text-blue-900',
    },
    success: {
      container: 'bg-green-50 border-green-200 text-green-800',
      icon: '✓',
      titleColor: 'text-green-900',
    },
    warning: {
      container: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      icon: '⚠️',
      titleColor: 'text-yellow-900',
    },
    error: {
      container: 'bg-red-50 border-red-200 text-red-800',
      icon: '✕',
      titleColor: 'text-red-900',
    },
  };

  const styles = variantStyles[variant];

  return (
    <div className={`border rounded-lg p-4 ${styles.container} ${className}`}>
      <div className="flex">
        <div className="flex-shrink-0 text-xl mr-3">{styles.icon}</div>
        <div className="flex-1">
          {title && (
            <h3 className={`text-sm font-semibold mb-1 ${styles.titleColor}`}>
              {title}
            </h3>
          )}
          <div className="text-sm">{children}</div>
        </div>
      </div>
    </div>
  );
}

