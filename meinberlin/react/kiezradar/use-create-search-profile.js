import { useState } from 'react'
import django from 'django'
import { updateItem } from '../contrib/helpers'

const errorCreatingSearchProfile = django.gettext(
  'Error creating search profile'
)

const STATUS_MAPPING = {
  running: 'active',
  done: 'past',
  future: 'future'
}

export function useCreateSearchProfile ({
  searchProfilesApiUrl,
  appliedFilters,
  districts,
  organisations,
  topicChoices,
  participationChoices,
  projectStatus,
  searchProfilesCount,
  onSearchProfileCreate
}) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [limitExceeded, setLimitExceeded] = useState(false)

  const createSearchProfile = async () => {
    if (searchProfilesCount === 10) {
      setLimitExceeded(true)
      return
    }

    setLoading(true)
    setError(null)

    const results = getFilteredResults({
      appliedFilters,
      districts,
      organisations,
      topicChoices,
      participationChoices,
      projectStatus
    })

    const {
      districtIds,
      organisationIds,
      topicIds,
      participationIds,
      projectStatusIds
    } = getFilteredIds(results)

    const params = {
      districts: districtIds,
      organisations: organisationIds,
      topics: topicIds,
      project_types: participationIds,
      status: projectStatusIds,
      plans_only: appliedFilters.plansOnly,
      notification: true
    }

    if (appliedFilters.search.length > 0) {
      params.query_text = appliedFilters.search
    }

    try {
      const response = await updateItem(params, searchProfilesApiUrl, 'POST')
      const searchProfile = await response.json()

      onSearchProfileCreate(searchProfile)
    } catch (err) {
      setError(errorCreatingSearchProfile)
    } finally {
      setLoading(false)
    }
  }

  return { loading, limitExceeded, error, createSearchProfile }
}

function getFilteredResults ({
  appliedFilters,
  districts,
  organisations,
  topicChoices,
  participationChoices,
  projectStatus
}) {
  return {
    filteredDistricts: districts.filter(district =>
      appliedFilters.districts.includes(district.name)
    ),
    filteredOrganisations: organisations.filter(organisation =>
      appliedFilters.organisation.includes(organisation.name)
    ),
    filteredTopics: topicChoices.filter(topic =>
      appliedFilters.topics.includes(topic.code)
    ),
    filteredParticipationChoices: appliedFilters.participations.map(index =>
      participationChoices[index]
    ),
    filteredProjectStatus: projectStatus.filter(status =>
      appliedFilters.projectState.includes(STATUS_MAPPING[status.name])
    )
  }
}

function getFilteredIds (results) {
  const filters = [
    results.filteredDistricts,
    results.filteredOrganisations,
    results.filteredTopics,
    results.filteredParticipationChoices,
    results.filteredProjectStatus
  ]

  const [
    districtIds,
    organisationIds,
    topicIds,
    participationIds,
    projectStatusIds
  ] = filters.map(items => items.map(item => item.id))

  return {
    districtIds,
    organisationIds,
    topicIds,
    participationIds,
    projectStatusIds
  }
}
