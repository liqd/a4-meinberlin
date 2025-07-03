import { getDistanceBetweenPoints } from '../contrib/helpers'

const isInTitle = (title, search) => {
  const titleLower = title?.toLowerCase().trim().replace(/\s/g, '') ?? ''
  const searchString = search.toLowerCase().trim()
  const searchList = searchString.split(/\s/)
  for (const i in searchList) {
    if (titleLower.indexOf(searchList[i]) === -1) {
      return false
    }
  }
  return true
}

const isInTopic = (topics, itemTopics, search) => {
  const activeTopics = topics.filter((topic) => itemTopics.includes(topic.code))
  return activeTopics.some(topic => isInTitle(topic.name, search))
}

const statusNames = ['active', 'future', 'past']

export const filterProjects = (items, appliedFilters, kiezradars, topics, projectState) => {
  const { search, topics: activeTopics, districts, organisation, participations, plansOnly, kiezradars: activeKiezradars } = appliedFilters

  const filterItem = (item) => {
    const isWithinAnyRadius =
      item.point && kiezradars.some(kiezradar =>
        activeKiezradars.includes(kiezradar.name) &&
        getDistanceBetweenPoints(item.point.geometry.coordinates, kiezradar.point.geometry.coordinates) <= kiezradar.radius
      )
    const hasKiezradarAndDistrict = activeKiezradars.length > 0 && districts.length > 0

    const hasRelevantOrEmptyActiveTopics = (activeTopics.length === 0 || activeTopics.some(topic => item.topics.includes(topic)))
    const hasRelevantOrEmptyParticipation = (participations.length === 0 || participations.includes(item.participation))
    const hasRelevantOrEmptyOrganisation = (organisation.length === 0 || organisation.includes(item.participation))

    const isTextSearchMatch = (search === '' ||
        isInTitle(item.title, search) ||
        isInTitle(item.district, search) ||
        isInTitle(item.organisation, search) ||
        isInTitle(item.description, search) ||
        isInTitle(item.identifier, search) ||
        isInTopic(topics, item.topics, search))

    const isStatusMatch = (projectState.includes(statusNames[item.status])) && (!plansOnly || item.type === 'plan')

    return (
      hasRelevantOrEmptyActiveTopics &&
      hasRelevantOrEmptyParticipation &&
      hasRelevantOrEmptyOrganisation &&
      isTextSearchMatch &&
      isStatusMatch &&
      (hasKiezradarAndDistrict
        // if we have both active we want to include projects that are within kiez
        // OR projects that are in the selected district
        ? (
            isWithinAnyRadius || districts.includes(item.district)
          )
        : (
            (activeKiezradars.length === 0 || isWithinAnyRadius) &&
            (districts.length === 0 || districts.includes(item.district))
          )
      )
    )
  }

  return items.filter(filterItem)
}
