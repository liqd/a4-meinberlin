import { renderHook } from '@testing-library/react'
import useNotifications from '../useNotifications'

describe('useNotifications hook', () => {
  const mockInitialNotifications = {
    email_newsletter: false,
    notify_followers_phase_started: true
  }

  test('initializes with correct state', () => {
    const { result } = renderHook(() => useNotifications(mockInitialNotifications, false))

    const {
      notificationsState,
      setNotificationsState,
      masterToggles
    } = result.current
    expect(notificationsState).toEqual(mockInitialNotifications)
    expect(typeof setNotificationsState).toBe('function')
    expect(Array.isArray(masterToggles)).toBe(true)
  })

  test('handles restricted notifications correctly', () => {
    const { result } = renderHook(() => useNotifications(mockInitialNotifications, true))

    const { masterToggles } = result.current
    expect(masterToggles.length).toBeGreaterThan(0)
  })
})
