const defaultState = {
  search: '',
  districts: [],
  // organisation is a single select but its simpler to just work with an
  // array because of the typeahead component
  organisation: [],
  participations: [],
  topics: [],
  plansOnly: false,
  kiezradars: []
}

export const getDefaultState = (searchParams, {
  districts,
  organisations,
  participationChoices,
  topicChoices,
  kiezradars
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
        .filter((participation) => searchParams.getAll('participations').includes(participation.value.toString()))
        .map((participation) => participation.value),
      topics: topicChoices
        .filter((topic) => searchParams.getAll('topics').includes(topic.code))
        .map((topic) => topic.code),
      plansOnly: searchParams.get('plansOnly') === 'true',
      kiezradars: kiezradars
        .filter(kiezradar => searchParams.getAll('kiezradars').includes(kiezradar.name))
        .map((kiezradar) => kiezradar.name)
    }
  }

  return {
    ...defaultState,
    ...mergeData
  }
}

const defaultProjectState = ['active', 'future']
export const validProjectStates = [...defaultProjectState, 'past']

export const getDefaultProjectState = (searchParams) => {
  const projectState = searchParams.getAll('projectState')
  const filteredStates = projectState.filter(state => validProjectStates.includes(state))

  return filteredStates.length ? filteredStates : defaultProjectState
}
