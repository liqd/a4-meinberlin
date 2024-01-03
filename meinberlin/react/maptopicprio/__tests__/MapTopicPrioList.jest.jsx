import React from 'react'
import { render, act, screen } from '@testing-library/react'
import { MapTopicPrioList } from '../MapTopicPrioList'
import { BrowserRouter } from 'react-router-dom'

// permissions
const permissions = {
  view_rate_count: true,
  view_comment_count: true
}

test('Map Topic Prioritisation list - check render with required stats',
  async () => {
    // sample data (one proposal item)
    const mockedResults = [
      {
        comment_count: 6,
        created: '2021-11-11T15:36:57.941072+01:00',
        creator: 'admin',
        is_archived: false,
        name: 'This is a topic',
        negative_rating_count: 1,
        pk: 7,
        positive_rating_count: 3,
        url: '/topic/2021-00007/'
      }
    ]

    // mimicking fetch response
    const mockedFetch = Promise.resolve({
      json: () => Promise.resolve({ results: mockedResults, permissions })
    })

    // overwrite global.fetch with mock function
    global.fetch = jest.fn().mockImplementation(() => mockedFetch)

    render(<BrowserRouter><MapTopicPrioList /></BrowserRouter>)
    expect(global.fetch).toHaveBeenCalledTimes(1)

    // waiting for async fetching ends --> without this, the
    // act(...) console.error will appear
    await act(() => mockedFetch)

    const comments = screen.getByText('Comments', { exact: false })
    const dislikes = screen.getByText('Dislikes', { exact: false })

    expect(screen.getByText('This is a topic')).toBeTruthy()
    expect(screen.getByText('LikeLikes')).toBeTruthy()
    expect(comments.textContent).toEqual('6CommentComments')
    expect(dislikes.textContent).toEqual('1DislikeDislikes')

    // reverse overwrite of global.fetch
    await global.fetch.mockClear()
  })
