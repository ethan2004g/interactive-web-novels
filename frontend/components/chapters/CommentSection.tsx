'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { readerService } from '@/services';
import { Comment } from '@/types';
import { useAuth } from '@/hooks';
import { LoadingSpinner } from '../common';

interface CommentSectionProps {
  chapterId: string;
}

interface CommentItemProps {
  comment: Comment;
  onReply: (commentId: string) => void;
  onDelete: (commentId: string) => void;
  currentUserId?: string;
}

function CommentItem({ comment, onReply, onDelete, currentUserId }: CommentItemProps) {
  const [showReplies, setShowReplies] = useState(false);

  const replies = comment.replies || [];
  const canDelete = currentUserId === comment.user?.id;

  return (
    <div className="mb-4">
      <div className="bg-gray-50 rounded-lg p-4">
        {/* Comment Header */}
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-gray-900">
              {comment.user?.username || 'Anonymous'}
            </span>
            <span className="text-sm text-gray-500">
              {new Date(comment.created_at).toLocaleDateString()}
            </span>
          </div>
          {canDelete && (
            <button
              onClick={() => onDelete(comment.id)}
              className="text-sm text-red-600 hover:text-red-700"
            >
              Delete
            </button>
          )}
        </div>

        {/* Comment Content */}
        <p className="text-gray-700 whitespace-pre-wrap mb-3">{comment.content}</p>

        {/* Comment Actions */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => onReply(comment.id)}
            className="text-sm text-blue-600 hover:text-blue-700"
          >
            Reply
          </button>
          {replies.length > 0 && (
            <button
              onClick={() => setShowReplies(!showReplies)}
              className="text-sm text-gray-600 hover:text-gray-700"
            >
              {showReplies ? 'Hide' : 'Show'} {replies.length} {replies.length === 1 ? 'reply' : 'replies'}
            </button>
          )}
        </div>
      </div>

      {/* Replies */}
      {showReplies && replies.length > 0 && (
        <div className="ml-8 mt-2 space-y-2">
          {replies.map((reply) => (
            <CommentItem
              key={reply.id}
              comment={reply}
              onReply={onReply}
              onDelete={onDelete}
              currentUserId={currentUserId}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function CommentSection({ chapterId }: CommentSectionProps) {
  const router = useRouter();
  const { user } = useAuth();
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [newComment, setNewComment] = useState('');
  const [replyingTo, setReplyingTo] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchComments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chapterId]);

  const fetchComments = async () => {
    try {
      const data = await readerService.getComments(chapterId);
      setComments(data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!user) {
      router.push('/auth/login');
      return;
    }

    if (!newComment.trim()) {
      return;
    }

    setSubmitting(true);
    try {
      await readerService.addComment(chapterId, newComment, replyingTo || undefined);
      setNewComment('');
      setReplyingTo(null);
      await fetchComments();
    } catch (error) {
      console.error('Error submitting comment:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleReply = (commentId: string) => {
    if (!user) {
      router.push('/auth/login');
      return;
    }
    setReplyingTo(commentId);
    // Scroll to comment form
    document.getElementById('comment-form')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleCancelReply = () => {
    setReplyingTo(null);
  };

  const handleDeleteComment = async (commentId: string) => {
    if (!window.confirm('Are you sure you want to delete this comment?')) {
      return;
    }

    try {
      await readerService.deleteComment(commentId);
      await fetchComments();
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };

  const topLevelComments = comments.filter((c) => !c.parent_comment_id);

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        Comments ({comments.length})
      </h2>

      {/* Comment Form */}
      {user ? (
        <form id="comment-form" onSubmit={handleSubmitComment} className="mb-8">
          {replyingTo && (
            <div className="mb-2 flex items-center justify-between bg-blue-50 p-2 rounded">
              <span className="text-sm text-blue-800">
                Replying to comment...
              </span>
              <button
                type="button"
                onClick={handleCancelReply}
                className="text-sm text-blue-600 hover:text-blue-700"
              >
                Cancel
              </button>
            </div>
          )}
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
            rows={4}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <div className="mt-3 flex justify-end">
            <button
              type="submit"
              disabled={submitting || !newComment.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? 'Posting...' : replyingTo ? 'Post Reply' : 'Post Comment'}
            </button>
          </div>
        </form>
      ) : (
        <div className="mb-8 bg-gray-50 rounded-lg p-6 text-center">
          <p className="text-gray-600 mb-4">
            You must be logged in to post comments.
          </p>
          <button
            onClick={() => router.push('/auth/login')}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Log In
          </button>
        </div>
      )}

      {/* Comments List */}
      {loading ? (
        <div className="flex justify-center py-8">
          <LoadingSpinner />
        </div>
      ) : topLevelComments.length === 0 ? (
        <p className="text-gray-600 text-center py-8">
          No comments yet. Be the first to comment!
        </p>
      ) : (
        <div className="space-y-4">
          {topLevelComments.map((comment) => (
            <CommentItem
              key={comment.id}
              comment={comment}
              onReply={handleReply}
              onDelete={handleDeleteComment}
              currentUserId={user?.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}

