import { renderHook, act } from '@testing-library/react'
import { updateItem } from '../contrib/helpers'
import { useCreateSearchProfile } from './use-create-search-profile'

jest.mock('../contrib/helpers', () => ({
  updateItem: jest.fn()
}))

describe('useCreateSearchProfile', () => {
  const searchProfilesApiUrl = '/api/search-profiles'
  const districts = [
    { id: 1, name: 'Charlottenburg-Wilmersdorf' },
    { id: 2, name: 'Friedrichshain-Kreuzberg' }
  ]
  const organisations = [{ id: 1, name: 'liqd' }]
  const topicChoices = [
    { id: 1, name: 'Anti-discrimination, Work & economy', code: 'ANT' }
  ]
  const participationChoices = [
    { id: 1, name: 'information (no participation)' },
    { id: 2, name: 'consultation' },
    { id: 3, name: 'cooperation' },
    { id: 4, name: 'decision-making' }
  ]
  const projectStatus = [
    {
      id: 1,
      status: 0,
      name: 'running'
    },
    {
      id: 2,
      status: 1,
      name: 'done'
    },
    {
      id: 3,
      status: 2,
      name: 'future'
    }
  ]
  const kiezradars = [
    { id: 1, name: 'Kiezradar 1' },
    { id: 2, name: 'Kiezradar 2' }
  ]

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('handles submission of a search profile', async () => {
    const appliedFilters = {
      districts: ['Charlottenburg-Wilmersdorf', 'Friedrichshain-Kreuzberg'],
      organisation: ['liqd'],
      topics: ['ANT'],
      participations: [3, 4],
      projectState: ['active', 'past', 'future'],
      kiezradars: ['Kiezradar 1', 'Kiezradar 2'],
      plansOnly: false,
      search: ''
    }

    const mockedData = {
      districts: [1, 2],
      organisations: [1],
      topics: [1],
      project_types: [3, 4],
      status: [1, 2, 3],
      kiezradars: [1, 2],
      plans_only: false,
      notification: true
    }

    const { result } = renderHook(() =>
      useCreateSearchProfile({
        searchProfilesApiUrl,
        appliedFilters,
        districts,
        organisations,
        topicChoices,
        participationChoices,
        projectStatus,
        kiezradars,
        searchProfilesCount: 0,
        onSearchProfileCreate: () => {}
      })
    )

    await act(async () => {
      await result.current.createSearchProfile()
    })

    expect(updateItem).toHaveBeenCalledWith(
      expect.objectContaining(mockedData),
      searchProfilesApiUrl,
      'POST'
    )
  })

  it('calls onSearchProfileCreate with searchProfile from updateItem', async () => {
    const appliedFilters = {
      districts: [],
      organisation: [],
      topics: [],
      participations: [],
      projectState: [],
      kiezradars: [],
      plansOnly: false,
      search: ''
    }

    const mockedSearchProfile = {
      id: 1,
      user: 1,
      name: 'Searchprofile 1',
      description: null,
      disabled: false,
      notification: false,
      status: [],
      query: 15,
      organisations: [],
      districts: [],
      project_types: [],
      topics: [],
      query_text: ''
    }

    jest.mocked(updateItem).mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce(mockedSearchProfile)
    })

    const mockOnSearchProfileCreate = jest.fn()

    const { result } = renderHook(() =>
      useCreateSearchProfile({
        searchProfilesApiUrl,
        appliedFilters,
        districts,
        organisations,
        topicChoices,
        participationChoices,
        projectStatus,
        kiezradars,
        searchProfilesCount: 0,
        onSearchProfileCreate: mockOnSearchProfileCreate
      })
    )

    await act(async () => {
      await result.current.createSearchProfile()
    })

    expect(mockOnSearchProfileCreate).toHaveBeenCalledWith(mockedSearchProfile)
  })

  it('sets limitExceeded to true when searchProfilesCount is 10', async () => {
    const appliedFilters = {
      districts: [],
      organisation: [],
      topics: [],
      participations: [],
      projectState: [],
      kiezradars: [],
      plansOnly: false,
      search: ''
    }

    const mockOnSearchProfileCreate = jest.fn()

    const { result } = renderHook(() =>
      useCreateSearchProfile({
        searchProfilesApiUrl,
        appliedFilters,
        districts,
        organisations,
        topicChoices,
        participationChoices,
        projectStatus,
        kiezradars,
        searchProfilesCount: 10,
        onSearchProfileCreate: mockOnSearchProfileCreate
      })
    )

    await act(async () => {
      await result.current.createSearchProfile()
    })

    expect(result.current.limitExceeded).toBe(true)
    expect(mockOnSearchProfileCreate).toHaveBeenCalledWith(null, true)
  })
})
