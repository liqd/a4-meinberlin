import django from 'django'
import { updateItem } from '../../contrib/assets/helpers.js'
import React from 'react'
import QuestionForm from './QuestionForm'
import QuestionList from './QuestionList'
import InfoBox from './InfoBox'
import Filters from './Filters'
import StatisticsBox from './StatisticsBox'

const selectAffiliationStr = django.gettext('select affiliation')
const informationStr = django.gettext('Information')
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
      categoryName: selectAffiliationStr,
      displayNotHiddenOnly: false,
      displayOnShortlist: false,
      orderedByLikes: false,
      filterChanged: false,
      orderingChanged: false,
      pollingPaused: false
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
    const newName = (category === '-1') ? selectAffiliationStr : category
    this.setState({
      filterChanged: true,
      categoryName: newName,
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
    this.timer = setInterval(() => this.getItems(), 5000)
  }

  render () {
    return (
      <div>
        <div className="tablist mb-0">
          <div className="container">
            <nav className="nav justify-content-center">
              <a
                id="tab-information"
                className="tab"
                data-bs-toggle="tab"
                href="#tabpanel-information"
                role="tab"
                aria-controls="tabpanel-information"
                aria-expanded="false"
              >
                {informationStr}
              </a>
              <a
                id="tab-questions"
                className="tab active"
                data-bs-toggle="tab"
                href="#tabpanel-questions"
                role="tab"
                aria-controls="tabpanel-questions"
                aria-expanded="true"
              >
                {questionsStr}
              </a>
              <a
                id="tab-statistics"
                className="tab"
                data-bs-toggle="tab"
                href="#tabpanel-statistics"
                role="tab"
                aria-controls="tabpanel-statistics"
                aria-expanded="false"
              >
                {statisticsStr}
              </a>
            </nav>
          </div>
        </div>
        <div
          className="tabpanel"
          id="tabpanel-information"
          role="tabpanel"
          aria-labelledby="tab-information"
          aria-hidden="false"
        >
          <div className="container">
            <div className="offset-lg-2 col-lg-8">
              {this.props.information}
            </div>
          </div>
        </div>

        <div
          className="tabpanel active"
          id="tabpanel-questions"
          role="tabpanel"
          aria-labelledby="tab-questions"
          aria-hidden="true"
        >
          {this.props.hasAskQuestionsPermission &&
            <div className="container">
              <div className="offset-lg-2 col-lg-8">
                <QuestionForm
                  restartPolling={this.restartPolling}
                  category_dict={this.props.category_dict}
                  questions_api_url={this.props.questions_api_url}
                  privatePolicyLabel={this.props.privatePolicyLabel}
                />
              </div>
            </div>}
          <div>
            <div className="container">
              <div className="offset-lg-2 col-lg-8">
                <InfoBox
                  isModerator={this.props.isModerator}
                />
                <div className="live_questions__filters--parent">
                  <Filters
                    categories={this.props.categories}
                    currentCategory={this.state.category}
                    currentCategoryName={this.state.categoryName}
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
                    <div>
                      <a className="btn btn--light live_questions__filters--screen-btn" rel="noopener noreferrer" href={this.props.present_url} target="_blank">
                        <span className="fa-stack fa-1x">
                          <i className="fas fa-tv fa-stack-2x" aria-label="hidden"> </i>
                          <i className="fas fa-arrow-up fa-stack-1x" aria-label="hidden"> </i>
                        </span>
                        {displayStr}
                      </a>
                    </div>}
                </div>
              </div>
            </div>
            <div className="module-content--light u-spacer-bottom">
              <div className="container">
                <div className="offset-lg-2 col-lg-8">
                  <QuestionList
                    questions={this.state.filteredQuestions}
                    removeFromList={this.removeFromList.bind(this)}
                    updateQuestion={this.updateQuestion.bind(this)}
                    handleLike={this.handleLike.bind(this)}
                    isModerator={this.props.isModerator}
                    togglePollingPaused={this.togglePollingPaused.bind(this)}
                    hasLikingPermission={this.props.hasLikingPermission}
                  />
                </div>
              </div>
            </div>
            <div className="live_questions__anchor">
              <span id="question-list-end" />
            </div>
          </div>
        </div>
        <div
          className="tabpanel module-content--light"
          id="tabpanel-statistics"
          role="tabpanel"
          aria-labelledby="tab-statistics"
          aria-hidden="false"
        >
          <StatisticsBox
            answeredQuestions={this.state.answeredQuestions}
            questions_api_url={this.props.questions_api_url}
            categories={this.props.categories}
            isModerator={this.props.isModerator}
          />
        </div>
      </div>
    )
  }
}
