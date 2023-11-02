import React from 'react'
import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ModeratorStatus } from '../ModeratorStatus'

describe('ModeratorStatus component', () => {
  test('renders without errors', () => {
    const badges = ['moderator_status', 'Accepted', 'ACCEPTED']
    render(<ModeratorStatus badges={badges} />)
  })

  test('displays the correct moderator status', () => {
    const badges = ['moderator_status', 'Accepted', 'ACCEPTED']
    const { getByText } = render(<ModeratorStatus badges={badges} />)
    const statusTextElement = getByText('Accepted')
    const statusText = statusTextElement.textContent
    // Check if "Accepted" is present
    expect(statusTextElement).toBeInTheDocument()
    // Check if "Accepted" is a string
    expect(typeof statusText).toBe('string')
  })
})
