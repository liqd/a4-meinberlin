import { ACTION_EVENT } from '../../../assets/js/action-events'
import { updateItem } from '../helpers'

describe('updateItem', () => {
  const originalFetch = global.fetch

  afterEach(() => {
    global.fetch = originalFetch
    jest.restoreAllMocks()
  })

  test('dispatches an action event for successful requests', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: true })
    const listener = jest.fn()
    document.addEventListener(ACTION_EVENT, listener)

    const response = await updateItem({ value: true }, '/api/example/', 'POST')

    expect(response.ok).toBe(true)
    expect(listener).toHaveBeenCalledTimes(1)
    expect(listener.mock.calls[0][0].detail).toEqual({
      url: '/api/example/',
      method: 'POST'
    })

    document.removeEventListener(ACTION_EVENT, listener)
  })

  test('does not dispatch an action event for failed requests', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: false })
    const listener = jest.fn()
    document.addEventListener(ACTION_EVENT, listener)

    await updateItem({ value: true }, '/api/example/', 'POST')

    expect(listener).not.toHaveBeenCalled()

    document.removeEventListener(ACTION_EVENT, listener)
  })
})
