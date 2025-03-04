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

  return items.filter((item) => {
    const isWithinAnyRadius =
      item.point && kiezradars.some(kiezradar =>
        activeKiezradars.includes(kiezradar.name) &&
        getDistanceBetweenPoints(item.point.geometry.coordinates, kiezradar.point.geometry.coordinates) <= kiezradar.radius
      )

    return (activeTopics.length === 0 || activeTopics.some(topic => item.topics.includes(topic))) &&
           (participations.length === 0 || participations.includes(item.participation)) &&
           (organisation.length === 0 || organisation.includes(item.organisation)) &&
           (search === '' ||
             isInTitle(item.title, search) ||
             isInTitle(item.district, search) ||
             isInTitle(item.organisation, search) ||
             isInTitle(item.description, search) ||
             isInTopic(topics, item.topics, search)) &&
           (projectState.includes(statusNames[item.status])) &&
           (!plansOnly || item.type === 'plan') &&
           (
             activeKiezradars.length === 0 || isWithinAnyRadius ||
             districts.length === 0 || districts.includes(item.district)
           )
  })
}
