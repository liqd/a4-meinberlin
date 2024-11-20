import django from 'django'
import { updateItem } from '../contrib/helpers.js'
import React, { useState, useEffect } from 'react'
import QuestionUser from './QuestionUser'
import QuestionModerator from './QuestionModerator'

const questionAnsweredTag = django.gettext('Questions Answered')
const categoriesTag = django.gettext('Categories')
const categoriesAnsweredTag = django.gettext('Affiliation Of Answered Questions')

function StatisticsBox (props) {
  const [answeredQuestions, setAnsweredQuestions] = useState(props.answeredQuestions)

  useEffect(() => {
    setAnsweredQuestions(props.answeredQuestions)
  }, [props.answeredQuestions])

  const updateQuestion = (data, id) => {
    const url = props.questions_api_url + id + '/'
    return updateItem(data, url, 'PATCH')
  }

  const removeFromList = (id, data) => {
    updateQuestion(data, id)
      .then(() => setAnsweredQuestions(prevQuestions => prevQuestions.filter(question => question.id !== id)
      ))
  }

  const countCategory = (category) => {
    let countPerCategory = 0
    let answeredQuestions = 0
    props.answeredQuestions.forEach(function (question) {
      if (question.is_answered && !question.is_hidden) {
        answeredQuestions++
        if (question.category === category) {
          countPerCategory++
        }
      }
    })
    return Math.round(countPerCategory * 100 / answeredQuestions) || 0
  }

  return (
    <div className="container">
      {Object.keys(props.category_dict).length > 0 && (
        <>
          <h2>{categoriesAnsweredTag}</h2>
          <div className="modul-card card">
            <h3>{categoriesTag}</h3>
            {Object.keys(props.category_dict).map((id) => {
              const countPerCategory = countCategory(props.category_dict[id])
              const style = { width: countPerCategory + '%' }
              return (
                <div className="live-question__progress" key={id}>
                  <div
                    className="live-question__progress-bar"
                    style={style}
                    role="progressbar"
                    aria-valuenow={countPerCategory}
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                  <div className="live-question__progress-text">
                    <span className="live-question__progress-percentage">
                      {countPerCategory}%
                    </span>{' '}
                    <span>{props.category_dict[id]}</span>
                  </div>
                </div>
              )
            })}
          </div>
        </>
      )}
      <h2>
        {questionAnsweredTag} ({answeredQuestions.length})
      </h2>
      {props.isModerator
        ? answeredQuestions.map((question) => (
          <QuestionModerator
            updateQuestion={updateQuestion}
            displayIsOnShortlist={false}
            displayIsLive={false}
            displayIsHidden={false}
            displayIsAnswered={question.is_answered}
            removeFromList={removeFromList}
            key={question.id}
            id={question.id}
            is_answered={question.is_answered}
            is_on_shortlist={question.is_on_shortlist}
            is_live={question.is_live}
            is_hidden={question.is_hidden}
            category={question.category}
            likes={question.likes}
            handleLike={props.handleLike.bind(this)}
            hasLikingPermission={props.hasLikingPermission}
          >
            {question.text}
          </QuestionModerator>
        ))
        : answeredQuestions.map((question) => (
          <QuestionUser
            key={question.id}
            id={question.id}
            is_answered={question.is_answered}
            is_on_shortlist={question.is_on_shortlist}
            is_live={question.is_live}
            is_hidden={question.is_hidden}
            category={question.category}
            likes={question.likes}
            handleLike={props.handleLike.bind(this)}
            hasLikingPermission={props.hasLikingPermission}
          >
            {question.text}
          </QuestionUser>
        ))}
    </div>
  )
}

export default StatisticsBox
