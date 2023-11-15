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
  const comments = screen.getByText('Comments', { exact: false })
  const dislikes = screen.getByText('Dislikes', { exact: false })
  // don't do same check for likes count as it also finds the
  // dislikes as non exact string but 1 count is enough
  expect(comments.textContent).toEqual('18Comments')
  expect(dislikes.textContent).toEqual('1Dislikes')
  expect(screen.getByText('Likes')).toBeTruthy()
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
  const comments = screen.getByText('Comments', { exact: false })
  const likes = screen.getByText('Support', { exact: false })

  expect(comments.textContent).toEqual('18Comments')
  expect(likes.textContent).toEqual('4Support')
  expect(screen.queryByText('Dislikes')).toBeNull()
  expect(screen.queryByText('Likes')).toBeNull()
  expect(screen.queryByText('Votes')).toBeNull()
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
  const comments = screen.getByText('Comments', { exact: false })
  const votes = screen.getByText('Votes', { exact: false })

  expect(comments.textContent).toEqual('18Comments')
  expect(votes.textContent).toEqual('7Votes')

  expect(screen.queryByText('Likes')).toBeNull()
  expect(screen.queryByText('Dislikes')).toBeNull()
})
