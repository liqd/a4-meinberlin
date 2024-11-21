import django from 'django'
import { updateItem } from '../contrib/helpers.js'
import React from 'react'
import QuestionForm from './QuestionForm'
import QuestionList from './QuestionList'
import Filters from './Filters'
import InfoBox from './InfoBox'
import StatisticsBox from './StatisticsBox'
import { IconSwitch } from '../contrib/IconSwitch'

const questionsStr = django.gettext('Questions')
const statisticsStr = django.gettext('Statistics')
const screenStr = django.gettext('Show on Screen')

export default class QuestionBox extends React.Component {
  constructor (props) {
    super(props)

    this.restartPolling = this.restartPolling.bind(this)

    this.state = {
      questions: [],
      filteredQuestions: [],
      answeredQuestions: [],
      filterChanged: false,
      filters: [],
      pollingPaused: false,
      showQuestions: true
    }
  }

  componentDidMount () {
    this.restartPolling()
  }

  componentWillUnmount () {
    this.timer = null
  }

  componentDidUpdate () {
    if (this.state.filterChanged === true) {
      this.updateList()
    }
  }

  isInFilter (item) {
    const filters = this.state.filters || {}
    const categories = filters.categories || []
    const markedFilter = filters.marked || []
    const displayFilter = filters.display || []

    const conditions = {
      bookmarked: item.is_on_shortlist,
      not_bookmarked: !item.is_on_shortlist,
      screen: item.is_live,
      not_screen: !item.is_live,
      answered: item.is_answered,
      not_answered: !item.is_answered,
      visible: !item.is_hidden,
      hidden: item.is_hidden
    }

    const matchesFilters = (filterGroup) => {
      if (filterGroup.length === 0) return true

      const filtersWithTrueConditions = filterGroup.map((filter) => conditions[filter])

      if (filtersWithTrueConditions.includes(undefined)) return true

      const allConflict = filtersWithTrueConditions.some((value) =>
        filtersWithTrueConditions.some((otherValue) => value !== otherValue)
      )

      if (allConflict) return true

      return filtersWithTrueConditions.every((condition) => condition)
    }

    const matchesCategoryFilter = categories.length === 0 || categories.includes(item.category)
    const matchesMarkedFilter = matchesFilters(markedFilter)
    const matchesDisplayFilter = matchesFilters(displayFilter)

    return (
      matchesCategoryFilter &&
      matchesMarkedFilter &&
      matchesDisplayFilter
    )
  }

  filterQuestions (questions) {
    const filteredQuestions = []
    questions.forEach((item) => {
      if (this.isInFilter(item) && (this.props.isModerator || !item.is_answered)) {
        filteredQuestions.push(item)
      }
    })
    return filteredQuestions
  }

  getAnsweredQuestions (questions) {
    const answeredQuestions = []
    questions.forEach((item) => {
      if (item.is_answered) {
        answeredQuestions.push(item)
      }
    })
    return answeredQuestions
  }

  updateList () {
    const filteredQuestions = this.filterQuestions(this.state.questions)
    this.setState({
      filterChanged: false,
      filteredQuestions
    })
  }

  getUrl () {
    return this.props.questions_api_url
  }

  getItems () {
    if (!this.state.pollingPaused) {
      fetch(this.getUrl())
        .then(response => response.json())
        .then(data => this.setState({
          questions: data,
          filteredQuestions: this.filterQuestions(data),
          answeredQuestions: this.getAnsweredQuestions(data)
        }))
    }
  }

  updateQuestion (data, id) {
    this.setState({
      pollingPaused: true
    })
    const url = this.props.questions_api_url + id + '/'
    return updateItem(data, url, 'PATCH')
  }

  removeFromList (id, data) {
    this.updateQuestion(data, id)
      .then(response => this.setState(prevState => ({
        filteredQuestions: prevState.filteredQuestions.filter(question => question.id !== id),
        pollingPaused: false
      })))
  }

  handleLike (id, value) {
    const url = '/api/questions/' + id + '/likes/'
    const data = { value }
    return updateItem(data, url, 'POST')
  }

  togglePollingPaused () {
    const pollingPaused = !this.state.pollingPaused
    this.setState({
      pollingPaused
    })
  }

  restartPolling () {
    this.getItems()
    clearInterval(this.timer)
    this.timer = setInterval(() => this.getItems(), 500)
  }

  applyFilters (filters) {
    this.setState({
      filters,
      filterChanged: true
    })
  }

  render () {
    return (
      <div className="live-question">
        {this.props.hasAskQuestionsPermission && (
          <QuestionForm
            restartPolling={this.restartPolling}
            category_dict={this.props.category_dict}
            questions_api_url={this.props.questions_api_url}
            privatePolicyLabel={this.props.privatePolicyLabel}
          />
        )}
        <div className="live-question__buttons">
          <IconSwitch
            className="live-question__icon-switch"
            buttons={[
              {
                label: questionsStr,
                icon: 'fa fa-list',
                id: 'show_questions',
                isActive: this.state.showQuestions,
                handleClick: () => {
                  this.setState({
                    showQuestions: true
                  })
                }
              },
              {
                label: statisticsStr,
                icon: 'fas fa-chart-bar',
                id: 'show_stats',
                isActive: !this.state.showQuestions,
                handleClick: () => {
                  this.setState({
                    showQuestions: false
                  })
                }
              }
            ]}
          />
          {this.props.isModerator && (
            <div>
              <a className="button button--light live-question__present" rel="noopener noreferrer" href={this.props.present_url} target="_blank">
                <span className="fas fa-tv mr-1" aria-hidden="true" />
                {screenStr}
              </a>
            </div>
          )}
        </div>
        {this.state.showQuestions
          ? (
            <>
              <InfoBox
                isModerator={this.props.isModerator}
              />
              <Filters
                categories={this.props.categories}
                isModerator={this.props.isModerator}
                onFiltered={this.applyFilters.bind(this)}
              />
              <QuestionList
                questions={this.state.filteredQuestions}
                removeFromList={this.removeFromList.bind(this)}
                updateQuestion={this.updateQuestion.bind(this)}
                handleLike={this.handleLike.bind(this)}
                isModerator={this.props.isModerator}
                togglePollingPaused={this.togglePollingPaused.bind(this)}
                hasLikingPermission={this.props.hasLikingPermission}
              />
            </>)
          : <StatisticsBox
              answeredQuestions={this.state.answeredQuestions}
              questions_api_url={this.props.questions_api_url}
              category_dict={this.props.category_dict}
              isModerator={this.props.isModerator}
            />}
      </div>
    )
  }
}
