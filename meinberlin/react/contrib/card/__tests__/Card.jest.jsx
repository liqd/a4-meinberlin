import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
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

  const commentsLabel = screen.getByText('Comments', { exact: false })

  // strings constructed by ngettext will render both options as jest does not mock ngettext functionality,
  // it just returns both so we check for both as it is a predicatble outcome
  // With <dl><dt><dd> structure, we need to get the parent div to access both dt and dd
  const comments = commentsLabel.closest('.stat-items')
  expect(comments.textContent).toEqual('7CommentComments')
  expect(screen.getByText('My idea')).toBeTruthy()
  expect(screen.getByText('Show')).toBeTruthy()
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

  const commentsLabel = screen.getByText('Comments', { exact: false })
  const dislikesLabel = screen.getByText('Dislikes', { exact: false })

  // With <dl><dt><dd> structure, we need to get the parent div to access both dt and dd
  const comments = commentsLabel.closest('.stat-items')
  const dislikes = dislikesLabel.closest('.stat-items')
  expect(comments.textContent).toEqual('7CommentComments')
  // don't do same check for likes count as it also finds the
  // dislikes as non exact string but 1 count is enough
  expect(dislikes.textContent).toEqual('1DislikeDislikes')
  expect(screen.getByText('My idea')).toBeTruthy()
  expect(screen.getByText('Show')).toBeTruthy()
})

test('clicking on the title triggers the click event on the link', () => {
  const idx = 123
  const item = { name: 'Example Item', url: 'https://example.com' }

  render(<Card idx={idx} item={item} permissions={[]} />)

  // Spy on the click method to check if it's called
  const clickSpy = jest.spyOn(document.getElementById('card-link-' + idx), 'click')

  const title = screen.getByText(item.name)
  fireEvent.click(title)

  // Assert that the click event on the link has been triggered
  expect(clickSpy).toHaveBeenCalled()

  // Clean up the spy
  clickSpy.mockRestore()
})
