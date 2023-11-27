import React from 'react'
import { render, screen, act } from '@testing-library/react'
import '@testing-library/jest-dom'
import { BrowserRouter } from 'react-router-dom'
import { MapIdeaList } from '../MapIdeaList' // Make sure to adjust the import path

test('MapIdeaList - fetch data', async () => {
  const permissions = {
    view_comment_count: true,
    view_rate_count: true
  }

  const mockedResults = [
    {
      additional_item_badges_for_list_count: 0,
      comment_count: 0,
      created: '2023-09-27T16:56:46.441086+02:00',
      creator: 'admin',
      item_badges_for_list: [['category', 'Category 1']],
      name: 'wee',
      negative_rating_count: 0,
      pk: 19,
      positive_rating_count: 0,
      reference_number: '2023-00019',
      url: '/mapideas/2023-00019/',
      point: "{'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': [13.29063, 52.475171]}}"
    },
    {
      additional_item_badges_for_list_count: 0,
      comment_count: 0,
      created: '2023-09-27T14:50:33.863235+02:00',
      creator: 'admin',
      item_badges_for_list: [
        ['category', 'Category 1'],
        ['label', 'Label 2']
      ],
      name: 'dswe',
      negative_rating_count: 0,
      pk: 11,
      positive_rating_count: 0,
      reference_number: '2023-00011',
      url: '/mapideas/2023-00011/',
      point: "{'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': [13.288499, 52.474203]}}"
    }
  ]

  const mockedFetch = Promise.resolve({
    json: () => Promise.resolve({ results: mockedResults, permissions })
  })

  // Overwrite global.fetch with mock function
  global.fetch = jest.fn().mockImplementation(() => mockedFetch)

  render(<BrowserRouter><MapIdeaList /></BrowserRouter>)
  expect(global.fetch).toHaveBeenCalledTimes(1)

  // Waiting for async fetching to end
  await act(async () => await mockedFetch)

  expect(screen.getByText('wee')).toBeTruthy()
  expect(screen.getByText('dswe')).toBeTruthy()

  // Check if badges are rendered
  const categoryElements = screen.getAllByText('Category 1')
  expect(categoryElements.length).toBeGreaterThanOrEqual(1)

  // Check if labels are rendered
  const labelElements = screen.getAllByText('Label 2')
  expect(labelElements.length).toBeGreaterThanOrEqual(1)

  // Reverse overwrite of global.fetch
  await global.fetch.mockClear()
})
