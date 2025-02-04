import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import NotificationsList from '../NotificationsList'
import { updateItem } from '../../contrib/helpers'
import useNotifications from '../useNotifications'

jest.mock('../../contrib/helpers', () => ({
  updateItem: jest.fn()
}))

jest.mock('../useNotifications', () => {
  return jest.fn()
})

const defaultProps = {
  initialNotifications: {
    email_newsletter: false,
    notify_followers_phase_started: true,
    track_followers_phase_started: false,
    notify_followers_phase_over_soon: false,
    notify_followers_event_upcoming: true,
    notify_creator: false,
    notify_creator_on_moderator_feedback: true,
    notify_initiators_project_created: false,
    notify_moderator: true
  },
  apiUrl: '/api/notifications/',
  showRestricted: false
}

describe('NotificationsList', () => {
  const mockSetNotificationsState = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    // Mock the default state of useNotifications
    useNotifications.mockImplementation((initialNotifications, showRestricted) => ({
      notificationsState: defaultProps.initialNotifications,
      setNotificationsState: mockSetNotificationsState,
      masterToggles: [true, false, false] // default master toggles state
    }))
  })

  test('renders all non-restricted notification groups', () => {
    render(<NotificationsList {...defaultProps} />)

    expect(screen.getByText('Project-Related Notifications')).toBeInTheDocument()
    expect(screen.getByText('Interactions with Other Users or Moderation')).toBeInTheDocument()
    expect(screen.queryByText('Notifications for Initiators and Moderators')).not.toBeInTheDocument()
  })

  test('renders restricted notifications when showRestricted is true', () => {
    useNotifications.mockImplementation((initialNotifications, showRestricted) => ({
      notificationsState: defaultProps.initialNotifications,
      setNotificationsState: mockSetNotificationsState,
      masterToggles: [true, false, false]
    }))

    render(<NotificationsList {...defaultProps} showRestricted />)

    expect(screen.getByText('Notifications for Initiators and Moderators')).toBeInTheDocument()
  })

  test('toggles individual notification settings', () => {
    render(<NotificationsList {...defaultProps} />)

    const toggle = screen.getAllByRole('checkbox')[1] // First toggle after master toggle
    fireEvent.click(toggle)

    expect(mockSetNotificationsState).toHaveBeenCalled()
    expect(updateItem).toHaveBeenCalledWith(
      { email_newsletter: true },
      '/api/notifications/',
      'PATCH'
    )
  })

  test('master toggle affects all notifications in group', () => {
    useNotifications.mockImplementation((initialNotifications, showRestricted) => ({
      notificationsState: defaultProps.initialNotifications,
      setNotificationsState: mockSetNotificationsState,
      masterToggles: [false, false, false]
    }))

    render(<NotificationsList {...defaultProps} />)

    const masterToggle = screen.getAllByRole('checkbox')[0]
    fireEvent.click(masterToggle)

    expect(mockSetNotificationsState).toHaveBeenCalled()
    expect(updateItem).toHaveBeenCalledWith(
      expect.objectContaining({
        email_newsletter: true,
        notify_followers_phase_started: true,
        notify_followers_phase_over_soon: true,
        notify_followers_event_upcoming: true
      }),
      '/api/notifications/',
      'PATCH'
    )
  })

  test('renders correct notification titles and descriptions', () => {
    render(<NotificationsList {...defaultProps} />)

    expect(screen.getByText('E-Mail Newsletter')).toBeInTheDocument()
    expect(screen.getByText('Participation Start')).toBeInTheDocument()
    expect(screen.getByText('Receive newsletters with updates and news about the projects you follow via e-mail.')).toBeInTheDocument()
  })

  test('updates UI and calls API when toggling notifications', async () => {
    render(<NotificationsList {...defaultProps} />)

    const toggle = screen.getAllByRole('checkbox')[1]
    fireEvent.click(toggle)

    expect(updateItem).toHaveBeenCalledWith(
      expect.objectContaining({ email_newsletter: true }),
      defaultProps.apiUrl,
      'PATCH'
    )

    await waitFor(() =>
      expect(mockSetNotificationsState)
        .toHaveBeenCalledWith(expect.objectContaining({ email_newsletter: true }))
    )
  })
})
