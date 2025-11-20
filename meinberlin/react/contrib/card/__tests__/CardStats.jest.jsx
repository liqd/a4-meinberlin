import React from 'react'
import { render, screen } from '@testing-library/react'
import { CardStats } from '../CardStats'

test('2 phase: rating phase - can view comments and ratings count', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: true,
    view_comment_count: true,
    view_vote_count: false
  }

  render(
    <CardStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
      voteCount="7"
    />
  )
  const commentsLabel = screen.getByText('Comments', { exact: false })
  const dislikesLabel = screen.getByText('Dislikes', { exact: false })
  // strings constructed by ngettext will render both options as jest does not mock ngettext functionality,
  // it just returns both so we check for both as it is a predicatble outcome
  // With <dl><dt><dd> structure, we need to get the parent div to access both dt and dd
  const comments = commentsLabel.closest('.stat-items')
  const dislikes = dislikesLabel.closest('.stat-items')
  expect(comments.textContent).toContain('18')
  expect(comments.textContent).toContain('Comment')
  expect(dislikes.textContent).toContain('1')
  expect(dislikes.textContent).toContain('Dislike')
  expect(screen.queryByText('Votes')).toBeNull()
})

test('3 phase: support phase - can view comments and support count', () => {
  const permissions = {
    view_support_count: true,
    view_rate_count: false,
    view_comment_count: true,
    view_vote_count: false
  }

  render(
    <CardStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
      voteCount="7"
    />
  )
  const commentsLabel = screen.getByText('Comments', { exact: false })
  const likesLabel = screen.getByText('Support', { exact: false })

  // With <dl><dt><dd> structure, we need to get the parent div to access both dt and dd
  const comments = commentsLabel.closest('.stat-items')
  const likes = likesLabel.closest('.stat-items')
  expect(comments.textContent).toContain('18')
  expect(comments.textContent).toContain('Comment')
  expect(likes.textContent).toContain('4')
  expect(likes.textContent).toContain('Supporter')
  expect(screen.queryByText('Dislikes')).toBeNull()
  expect(screen.queryByText('Likes')).toBeNull()
  expect(screen.queryByText('Votes')).toBeNull()
  expect(screen.queryByText('1 Dislikes')).toBeNull()
  expect(screen.queryByText('7 VoteVotes')).toBeNull()
})

test('3 phase: finished - can view comments and vote count', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: false,
    view_comment_count: true,
    view_vote_count: true
  }

  render(
    <CardStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
      voteCount="7"
    />
  )
  const commentsLabel = screen.getByText('Comments', { exact: false })
  const votesLabel = screen.getByText('Votes', { exact: false })

  // With <dl><dt><dd> structure, we need to get the parent div to access both dt and dd
  const comments = commentsLabel.closest('.stat-items')
  const votes = votesLabel.closest('.stat-items')
  expect(comments.textContent).toContain('18')
  expect(comments.textContent).toContain('Comment')
  expect(votes.textContent).toContain('7')
  expect(votes.textContent).toContain('Vote')
  expect(screen.queryByText('Likes')).toBeNull()
  expect(screen.queryByText('Dislikes')).toBeNull()
  expect(screen.queryByText('4 Likes')).toBeNull()
  expect(screen.queryByText('1 Dislikes')).toBeNull()
})
