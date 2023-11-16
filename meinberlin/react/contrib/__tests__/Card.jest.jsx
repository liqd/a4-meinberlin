import React from 'react'
import { render, screen } from '@testing-library/react'
import { Card } from '../Card'

test('Card component with item name and link and comment count', () => {
  const permissions = {
    view_rate_count: false,
    view_comment_count: true,
    view_support_count: false,
    view_vote_count: false,
    vote_allowed: false,
    has_voting_permission_and_valid_token: false
  }

  const proposal = {
    name: 'My idea',
    url: 'www.example.com',
    positive_rating_count: 2,
    negative_rating_count: 1,
    comment_count: 7
  }

  render(
    <Card item={proposal} permissions={permissions} />
  )

  const comments = screen.getByText('Comments', { exact: false })

  // strings constructed by ngettext will render both options as jest does not mock ngettext functionality,
  // it just returns both so we check for both as it is a predicatble outcome
  expect(comments.textContent).toEqual('7CommentComments')
  expect(screen.getByText('My idea')).toBeTruthy()
  expect(screen.getByText('Item details')).toBeTruthy()
  expect(screen.queryByText('Likes')).toBeNull()
  expect(screen.queryByText('Votes')).toBeNull()
})

test('Renders a link to item details', () => {
  const permissions = {
    view_rate_count: true,
    view_comment_count: true,
    view_support_count: false,
    view_vote_count: false,
    vote_allowed: false,
    has_voting_permission_and_valid_token: false
  }

  const proposal = {
    name: 'My idea',
    url: 'www.example.com',
    positive_rating_count: 2,
    negative_rating_count: 1,
    comment_count: 7
  }

  render(
    <Card item={proposal} permissions={permissions} />
  )

  const comments = screen.getByText('Comments', { exact: false })
  const dislikes = screen.getByText('Dislikes', { exact: false })

  expect(comments.textContent).toEqual('7CommentComments')
  // don't do same check for likes count as it also finds the
  // dislikes as non exact string but 1 count is enough
  expect(dislikes.textContent).toEqual('1Dislikes')
  expect(screen.getByText('My idea')).toBeTruthy()
  expect(screen.getByText('Item details')).toBeTruthy()
})
