import { getDistanceBetweenPoints } from '../contrib/helpers'

export const isInTitle = (title, search) => {
  const titleLower = title.toLowerCase().trim().replace(/\s/g, '')
  const searchString = search.toLowerCase().trim()
  const searchList = searchString.split(/\s/)
  for (const i in searchList) {
    if (titleLower.indexOf(searchList[i]) === -1) {
      return false
    }
  }
  return true
}

const statusNames = ['active', 'future', 'past']

export const filterProjects = (items, appliedFilters, kiezradars, projectState) => {
  const { search, topics, districts, organisation, participations, plansOnly, kiezradars: activeKiezradars } = appliedFilters

  return items.filter((item) => {
    const isWithinAnyRadius =
      item.point && kiezradars.some(kiezradar =>
        activeKiezradars.includes(kiezradar.name) &&
        getDistanceBetweenPoints(item.point.geometry.coordinates, kiezradar.point.geometry.coordinates) <= kiezradar.radius
      )

    return (topics.length === 0 || topics.some(topic => item.topics.includes(topic))) &&
           (districts.length === 0 || districts.includes(item.district)) &&
           (participations.length === 0 || participations.includes(item.participation)) &&
           (organisation.length === 0 || organisation.includes(item.organisation)) &&
           (search === '' || isInTitle(item.title, search)) &&
           (projectState.includes(statusNames[item.status])) &&
           (!plansOnly || item.type === 'plan') &&
           (activeKiezradars.length === 0 || isWithinAnyRadius)
  })
}
