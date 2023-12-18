import React from 'react'
import {
  fireEvent,
  render,
  screen
} from '@testing-library/react'
import { ControlBar } from '../ControlBar'
import { BrowserRouter } from 'react-router-dom'

const filters = {
  category: {
    label: 'categories',
    current: 'all',
    icons: [['1', 'some/url']],
    choices: [['1', 'all'], ['2', 'category1']]
  },
  labels: {
    label: 'labels',
    current: 'all',
    icons: [['1', 'some/url']],
    choices: [['1', 'all'], ['2', 'label1'], ['3', 'label2']]
  },
  tasks: {
    label: 'tasks',
    current: 'all',
    icons: [['1', 'some/url']],
    choices: [['1', 'all'], ['2', 'task1'], ['3', 'task2']]
  },
  status: {
    label: 'status',
    current: 'all',
    icons: [['1', 'some/url']],
    choices: [['1', 'all'], ['2', 'status1'], ['3', 'status2']]
  },
  ordering: {
    label: 'ordering',
    current: 'Most recent',
    choices: [['latest', 'Most recent'], ['most', 'Most voted']]
  }
}

jest.mock('../contexts/FetchItemsProvider', () => ({
  useFetchedItems: jest.fn(() => ({
    results: { map: { filters }, list: { filters } },
    currentPage: 1,
    isMapAndList: true,
    viewMode: 'list'
  }))
}))

test('ControlBar shown when list is empty', () => {
  render(
    <BrowserRouter>
      <ControlBar />
    </BrowserRouter>
  )
  const numOfResultsElement = screen.queryByText(/found/)
  expect(numOfResultsElement).toBeFalsy()
  const orderingFilterElement = screen.getByText('Most recent')
  expect(orderingFilterElement).toBeTruthy()
})

test('ControlBar expanded by default', async () => {
  render(
    <BrowserRouter>
      <ControlBar />
    </BrowserRouter>
  )
  const categories = screen.getByText(/categories/)
  const labels = screen.getByText(/labels/)
  const task = screen.getByText(/tasks/)
  let status = screen.getByText('status')
  expect(categories).toBeTruthy()
  expect(labels).toBeTruthy()
  expect(task).toBeTruthy()
  expect(status).toBeTruthy()
  const filterButton = screen.getByRole('button', { name: /show less/i })
  fireEvent.click(filterButton)
  status = screen.queryByText('status')
  expect(status).not.toBeTruthy()
})

test('ControlBar filters create pills', async () => {
  render(
    <BrowserRouter>
      <ControlBar />
    </BrowserRouter>
  )
  const categories = screen.getByLabelText(/categories/)
  expect(categories).toBeTruthy()
  fireEvent.change(categories, { target: { value: '2' } })
  fireEvent.click(screen.getByRole('button', { name: /filter/ }))
  const category = screen.getAllByText('categories')
  expect(category).toHaveLength(2)
})
