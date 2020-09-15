import django from 'django'
import { updateItem } from './helpers.js'
import React from 'react'
import QuestionUser from './QuestionUser'
import QuestionModerator from './QuestionModerator'

export default class StatisticsBox extends React.Component {
  constructor (props) {
    super(props)
    this.state = { answeredQuestions: props.answeredQuestions }
  }

  componentWillReceiveProps (props) {
    this.setState({ answeredQuestions: props.answeredQuestions })
  }

  updateQuestion (data, id) {
    const url = this.props.questions_api_url + id + '/'
    return updateItem(data, url, 'PATCH')
  }

  removeFromList (id, data) {
    this.updateQuestion(data, id)
      .then(response => this.setState(prevState => ({
        answeredQuestions: prevState.answeredQuestions.filter(question => question.id !== id)
      })))
  }

  countCategory (category) {
    let countPerCategory = 0
    let answeredQuestions = 0
    this.props.answeredQuestions.forEach(function (question) {
      if (question.is_answered && !question.is_hidden) {
        answeredQuestions++
        if (question.category === category) {
          countPerCategory++
        }
      }
    })
    return Math.round(countPerCategory * 100 / answeredQuestions) || 0
  }

  render () {
    const questionAnsweredTag = django.gettext('Questions Answered')
    const categoriesAnswerdTag = django.gettext('Categories Answered')
    return (
      <div className="module-content">
        <div className="l-wrapper">
          <div className="l-center-8">
            <h3>{categoriesAnsweredTag}</h3>
            <div className="list-item list-item--squashed">
              {this.props.categories.map((category, index) => {
                const countPerCategory = this.countCategory(category)
                const style = { width: countPerCategory + '%' }
                return (
                  <div key={index} className="u-spacer-bottom-half">
                    <div className="progress">
                      <div
                        className="progress-bar" style={style} role="progressbar" aria-valuenow="25" aria-valuemin="0"
                        aria-valuemax="100"
                      ><span>&nbsp;{category}&nbsp;</span>{countPerCategory}%
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
            <h3>{questionAnsweredTag}</h3>
            {this.props.isModerator
              ? (
                <div className="list-group">
                  {this.state.answeredQuestions.map((question, index) => {
                    return (
                      <QuestionModerator
                        updateQuestion={this.updateQuestion.bind(this)}
                        displayIsOnShortlist={false}
                        displayIsLive={false}
                        displayIsHidden={false}
                        displayIsAnswered={question.is_answered}
                        removeFromList={this.removeFromList.bind(this)}
                        key={question.id}
                        id={question.id}
                        is_answered={question.is_answered}
                        is_on_shortlist={question.is_on_shortlist}
                        is_live={question.is_live}
                        is_hidden={question.is_hidden}
                        category={question.category}
                        likes={question.likes}
                      >
                        {question.text}
                      </QuestionModerator>
                    )
                  })}
                </div>
              )
              : (
                <div className="list-group">
                  {this.state.answeredQuestions.map((question, index) => {
                    return (
                      <QuestionUser
                        key={question.id}
                        id={question.id}
                        is_answered={question.is_answered}
                        is_on_shortlist={question.is_on_shortlist}
                        is_live={question.is_live}
                        is_hidden={question.is_hidden}
                        category={question.category}
                        likes={question.likes}
                      >
                        {question.text}
                      </QuestionUser>
                    )
                  })}
                </div>
              )}
          </div>
        </div>
      </div>
    )
  }
}
