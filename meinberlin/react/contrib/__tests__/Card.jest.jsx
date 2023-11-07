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
  expect(screen.getByText('My idea')).toBeTruthy()
  expect(screen.getByText('Item details')).toBeTruthy()
  expect(screen.getByText('7 Comments')).toBeTruthy()
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
  expect(screen.getByText('My idea')).toBeTruthy()
  expect(screen.getByText('Item details')).toBeTruthy()
  expect(screen.getByText('7 Comments')).toBeTruthy()
  expect(screen.getByText('2 Likes')).toBeTruthy()
  expect(screen.getByText('1 Dislikes')).toBeTruthy()
})
