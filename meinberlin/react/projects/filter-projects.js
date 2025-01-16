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

export const filterProjects = (items, appliedFilters) => {
  const { search, topics, districts, organisation, participations, plansOnly } = appliedFilters

  return items.filter((item) => {
    return (topics.length === 0 || topics.some(topic => item.topics.includes(topic))) &&
           (districts.length === 0 || districts.includes(item.district)) &&
           (participations.length === 0 || participations.includes(item.participation)) &&
           (organisation.length === 0 || organisation.includes(item.organisation)) &&
           (search === '' || isInTitle(item.title, search)) &&
           (!plansOnly || item.type === 'plan')
  })
}
