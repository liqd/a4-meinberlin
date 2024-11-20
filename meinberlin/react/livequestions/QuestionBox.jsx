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
const displayStr = django.gettext('display on screen')

export default class QuestionBox extends React.Component {
  constructor (props) {
    super(props)

    this.restartPolling = this.restartPolling.bind(this)

    this.state = {
      questions: [],
      filteredQuestions: [],
      answeredQuestions: [],
      category: '-1',
      displayNotHiddenOnly: false,
      displayOnShortlist: false,
      orderedByLikes: false,
      filterChanged: false,
      orderingChanged: false,
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
    if (this.state.orderingChanged === true) {
      this.getItems()
    }
  }

  setCategory (category) {
    this.setState({
      filterChanged: true,
      category
    })
  }

  toggledisplayNotHiddenOnly () {
    const displayNotHiddenOnly = !this.state.displayNotHiddenOnly
    this.setState({
      filterChanged: true,
      displayNotHiddenOnly
    })
  }

  toggleDisplayOnShortlist () {
    const displayOnShortlist = !this.state.displayOnShortlist
    this.setState({
      filterChanged: true,
      displayOnShortlist
    })
  }

  toggleOrdering () {
    const orderedByLikes = !this.state.orderedByLikes
    this.setState({
      orderingChanged: true,
      orderedByLikes
    })
  }

  isInFilter (item) {
    return (this.state.category === '-1' || this.state.category === item.category) &&
      (!this.state.displayOnShortlist || item.is_on_shortlist) && (!this.state.displayNotHiddenOnly || !item.is_hidden)
  }

  filterQuestions (questions) {
    const filteredQuestions = []
    questions.forEach((item) => {
      if (this.isInFilter(item) && !item.is_answered) {
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
    const url = this.props.questions_api_url
    if (this.state.orderedByLikes) {
      return url + '?ordering=-like_count'
    }
    return url
  }

  getItems () {
    if (!this.state.pollingPaused) {
      fetch(this.getUrl())
        .then(response => response.json())
        .then(data => this.setState({
          questions: data,
          filteredQuestions: this.filterQuestions(data),
          answeredQuestions: this.getAnsweredQuestions(data),
          orderingChanged: false
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
        {this.state.showQuestions
          ? (
            <>
              <InfoBox
                isModerator={this.props.isModerator}
              />
              <Filters
                categories={this.props.categories}
                currentCategory={this.state.category}
                setCategories={this.setCategory.bind(this)}
                orderedByLikes={this.state.orderedByLikes}
                toggleOrdering={this.toggleOrdering.bind(this)}
                displayOnShortlist={this.state.displayOnShortlist}
                displayNotHiddenOnly={this.state.displayNotHiddenOnly}
                toggleDisplayOnShortlist={this.toggleDisplayOnShortlist.bind(this)}
                toggledisplayNotHiddenOnly={this.toggledisplayNotHiddenOnly.bind(this)}
                isModerator={this.props.isModerator}
              />
              {this.props.isModerator &&
                <div className="block">
                  <a className="btn btn--light" rel="noopener noreferrer" href={this.props.present_url} target="_blank">
                    <span className="fa-stack fa-1x">
                      <i className="fas fa-tv fa-stack-2x" aria-label="hidden"> </i>
                      <i className="fas fa-arrow-up fa-stack-1x" aria-label="hidden"> </i>
                    </span>
                    {displayStr}
                  </a>
                </div>}
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
              handleLike={this.handleLike.bind(this)}
              hasLikingPermission={this.props.hasLikingPermission}
            />}
      </div>
    )
  }
}
