const defaultState = {
  search: '',
  districts: [],
  // organisation is a single select but its simpler to just work with an
  // array because of the typeahead component
  organisation: [],
  participations: [],
  topics: [],
  plansOnly: false
}

export const getDefaultState = (searchProfile) => {
  let mergeData = {}

  if (searchProfile) {
    mergeData = {
      search: searchProfile.query_text ?? '',
      districts: searchProfile.districts.map(d => d.name),
      organisation: searchProfile.organisations.map(o => o.name),
      participations: searchProfile.project_types.map(p => p.id),
      topics: searchProfile.topics.map((t) => t.code)
    }
  }

  return {
    ...defaultState,
    ...mergeData
  }
}

export const getDefaultProjectState = (searchProfile) => {
  const mapping = ['active', 'past', 'future']
  if (searchProfile && searchProfile.status.length) {
    return searchProfile.status.map(s => mapping[s.status])
  }

  return ['active', 'future']
}
