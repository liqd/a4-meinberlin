import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import { Pagination } from '../Pagination'
import { BrowserRouter } from 'react-router'

test('clicking on page 2 sets button to active', () => {
  render(
    <BrowserRouter>
      <Pagination
        currentPage={1}
        elidedRange={[1, 2, '…', 3]}
      />
    </BrowserRouter>
  )
  const pageButton2 = screen.getByText('2')
  fireEvent.click(pageButton2)
  const parentPageButton2 = screen.getByText('2').closest('li button')
  expect(parentPageButton2.className).toBe('active')
})
