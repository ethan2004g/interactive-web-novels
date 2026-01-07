import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 sm:text-6xl">
            Interactive Web Novels
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            Create and read interactive stories with branching storylines, visual effects,
            and immersive experiences. Where traditional storytelling meets code.
          </p>
          <div className="mt-10 flex justify-center gap-4">
            <Link
              href="/auth/register"
              className="px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:text-lg"
            >
              Get Started
            </Link>
            <Link
              href="/books"
              className="px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 md:text-lg"
            >
              Browse Books
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* For Readers */}
          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="text-blue-600 text-3xl mb-4">📚</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">For Readers</h3>
            <p className="text-gray-600">
              Discover interactive stories where your choices matter. Experience visual
              effects, branching storylines, and immersive narratives.
            </p>
          </div>

          {/* For Authors */}
          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="text-blue-600 text-3xl mb-4">✍️</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">For Authors</h3>
            <p className="text-gray-600">
              Write traditional chapters or code interactive experiences. Create branching
              paths, add animations, and bring your stories to life.
            </p>
          </div>

          {/* Interactive */}
          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="text-blue-600 text-3xl mb-4">🎮</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Interactive</h3>
            <p className="text-gray-600">
              Visual novel elements, custom styling, embedded media, and code snippets.
              Stories that feel like games.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Your Journey?</h2>
          <p className="text-xl mb-8 text-blue-100">
            Join our community of readers and authors today.
          </p>
          <Link
            href="/auth/register"
            className="inline-block px-8 py-3 border-2 border-white text-base font-medium rounded-md text-white hover:bg-white hover:text-blue-600 transition-colors md:text-lg"
          >
            Sign Up Now
          </Link>
        </div>
      </section>
    </div>
  );
}
