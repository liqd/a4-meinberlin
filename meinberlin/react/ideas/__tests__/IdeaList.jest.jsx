import React from 'react'
import { render, screen, act } from '@testing-library/react'
import '@testing-library/jest-dom'
import { BrowserRouter } from 'react-router-dom'
import { IdeaList } from '../IdeaList'

test('Idea List - fetch data', async () => {
  const permissions = {
    view_comment_count: true,
    view_rate_count: true
  }

  const mockedResults = [
    {
      comment_count: 6,
      created: '2023-11-15T15:36:57.941072+01:00',
      creator: 'admin',
      is_archived: false,
      name: 'Idea 1',
      negative_rating_count: 1,
      pk: 7,
      positive_rating_count: 3,
      url: '/Idea/2023-00017/',
      additional_item_badges_for_list_count: 1,
      get_moderator_status_display: 'Qualified for next phase',
      moderator_status: 'QUALIFIED',
      item_badges_for_list: [
        ['label', 'Label 2'], ['category', 'Category 1']]
    }
  ]

  const mockedFetch = Promise.resolve({
    json: () => Promise.resolve({ results: mockedResults, permissions })
  })

  // Overwrite global.fetch with mock function
  global.fetch = jest.fn().mockImplementation(() => mockedFetch)

  render(<BrowserRouter><IdeaList /></BrowserRouter>)
  expect(global.fetch).toHaveBeenCalledTimes(1)

  // Waiting for async fetching ends --> without this, the
  // act(...) console.error will appear
  await act(async () => await mockedFetch)
  expect(screen.getByText('Idea 1')).toBeTruthy() // Adjust text based on your component content

  // Check if comment count is rendered
  expect(screen.getByText('6 Comments')).toBeTruthy()

  // Check if pills are rendered
  expect(screen.getByText('Category 1')).toBeTruthy()
  expect(screen.getByText('Label 2')).toBeTruthy()

  // Check status
  expect(screen.getByText('Qualified for next phase')).toBeTruthy()

  // Reverse overwrite of global.fetch
  await global.fetch.mockClear()
})
