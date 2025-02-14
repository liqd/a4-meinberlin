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

export const getDefaultState = (searchParams, {
  districts,
  organisations,
  participationChoices,
  topicChoices
}) => {
  let mergeData = {}

  if (searchParams) {
    mergeData = {
      search: searchParams.get('search') ?? '',
      districts: districts
        .filter((district) => searchParams.getAll('districts').includes(district.name))
        .map((district) => district.name),
      organisation: organisations
        .filter((organisation) => searchParams.getAll('organisation').includes(organisation.name))
        .map((organisation) => organisation.name),
      participations: participationChoices
        .filter((participation) => searchParams.getAll('participations').includes(participation.id.toString()))
        .map((participation) => participation.id),
      topics: topicChoices
        .filter((topic) => searchParams.getAll('topics').includes(topic.code))
        .map((topic) => topic.code),
      plansOnly: searchParams.get('plansOnly') === 'true'
    }
  }

  return {
    ...defaultState,
    ...mergeData
  }
}

const defaultProjectState = ['active', 'future']
const validProjectStates = [...defaultProjectState, 'past']

export const getDefaultProjectState = (searchParams) => {
  const projectState = searchParams.getAll('projectState')
  const filteredStates = projectState.filter(state => validProjectStates.includes(state))

  return filteredStates.length ? filteredStates : defaultProjectState
}
