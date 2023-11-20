import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import { ControlBarFilterPills } from '../ControlBarFilterPills'

describe('ControlBarFilterPills', () => {
  const removeFn = jest.fn()

  const props = {
    onRemove: removeFn,
    filters: [
      { type: 'color', value: 'red', label: 'Red' },
      { type: 'size', value: 'large', label: 'Large' }
    ]
  }

  test('renders filters and removes filter on button click', () => {
    render(<ControlBarFilterPills {...props} />)

    // Check if the filters render
    expect(screen.getByText('Red')).toBeTruthy()
    expect(screen.getByText('Large')).toBeTruthy()

    // Simulate clicking the close button
    fireEvent.click(screen.getAllByRole('button')[0])

    // Check if the remove function was called with the correct argument
    expect(removeFn).toHaveBeenCalledWith('color')
  })

  test('does not render if filters are empty or values are empty strings', () => {
    const removeFn = jest.fn()
    const emptyFilters = [{ type: 'color', value: '', label: 'Red' }]

    const { container } = render(<ControlBarFilterPills filters={emptyFilters} onRemove={removeFn} />)
    expect(container.firstChild).toBeNull()
  })
})
