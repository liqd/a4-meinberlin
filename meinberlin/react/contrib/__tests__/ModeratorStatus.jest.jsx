import React from 'react'
import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ModeratorStatus } from '../ModeratorStatus'

describe('ModeratorStatus component', () => {
  test('renders without errors when modStatus is present', () => {
    render(<ModeratorStatus modStatus="ACCEPTED" modStatusDisplay="Accepted" />)
  })

  test('displays the correct moderator status', () => {
    const modStatus = 'STATUS'
    const modStatusDisplay = 'Accepted'
    const { getByText } = render(<ModeratorStatus modStatus={modStatus} modStatusDisplay={modStatusDisplay} />)
    const statusTextElement = getByText('Accepted')
    const statusText = statusTextElement.textContent
    // Check if "Accepted" is present
    expect(statusTextElement).toBeInTheDocument()
    // Check if "Accepted" is a string
    expect(typeof statusText).toBe('string')
  })
})
