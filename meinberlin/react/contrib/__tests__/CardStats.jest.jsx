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
  expect(screen.getByText('4 Likes')).toBeTruthy()
  expect(screen.getByText('1 Dislikes')).toBeTruthy()
  expect(screen.getByText('18 Comments')).toBeTruthy()
  expect(screen.queryByText('7 Votes')).toBeNull()
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
  expect(screen.getByText('4 Support')).toBeTruthy()
  expect(screen.queryByText('1 Dislikes')).toBeNull()
  expect(screen.getByText('18 Comments')).toBeTruthy()
  expect(screen.queryByText('7 Votes')).toBeNull()
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
  expect(screen.queryByText('4 Likes')).toBeNull()
  expect(screen.queryByText('1 Dislikes')).toBeNull()
  expect(screen.getByText('18 Comments')).toBeTruthy()
  expect(screen.getByText('7 Votes')).toBeTruthy()
})
