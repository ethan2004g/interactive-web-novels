interface SkeletonLoaderProps {
  variant?: 'text' | 'card' | 'avatar' | 'rectangle';
  width?: string;
  height?: string;
  className?: string;
}

export function SkeletonLoader({
  variant = 'text',
  width,
  height,
  className = '',
}: SkeletonLoaderProps) {
  const baseClasses = 'animate-pulse bg-gray-200 rounded';

  const variantClasses = {
    text: 'h-4 w-full',
    card: 'h-48 w-full',
    avatar: 'h-12 w-12 rounded-full',
    rectangle: 'h-32 w-full',
  };

  const style = {
    width: width || undefined,
    height: height || undefined,
  };

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      style={style}
    />
  );
}

export function BookCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <SkeletonLoader variant="rectangle" height="200px" />
      <div className="p-4 space-y-3">
        <SkeletonLoader variant="text" height="24px" />
        <SkeletonLoader variant="text" height="16px" width="60%" />
        <SkeletonLoader variant="text" height="16px" width="40%" />
      </div>
    </div>
  );
}

export function ChapterListSkeleton() {
  return (
    <div className="space-y-2">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="flex items-center space-x-3 p-3 bg-white rounded-lg">
          <SkeletonLoader variant="rectangle" width="40px" height="40px" />
          <div className="flex-1 space-y-2">
            <SkeletonLoader variant="text" height="20px" width="70%" />
            <SkeletonLoader variant="text" height="14px" width="40%" />
          </div>
        </div>
      ))}
    </div>
  );
}

