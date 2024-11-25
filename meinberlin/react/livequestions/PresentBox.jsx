import React, { useEffect } from 'react'
import QuestionPresent from './QuestionPresent'

const PresentBox = (props) => {
  const [questions, setQuestions] = React.useState([])

  const getQuestions = () => {
    fetch(props.questions_api_url + '?is_live=1&is_answered=0')
      .then(response => handleErrors(response))
      .then(response => response.json())
      .then(data => setQuestions(data))
      .catch(error => {
        console.error('Error fetching questions:', {
          message: error.message,
          stack: error.stack,
          apiUrl: props.questions_api_url
        })
      })
  }

  const handleErrors = (response) => {
    if (!response.ok) {
      throw new Error('HTTP-Error:' + response.status + '-' + response.statusText)
    }
    return response
  }

  const removeUserIndicator = () => {
    const userIndicator = document.getElementById('layout-grid__area--contentheader')
    if (userIndicator) {
      userIndicator.remove()
    }
  }

  useEffect(() => {
    removeUserIndicator()
    getQuestions()

    const intervalId = setInterval(() => {
      getQuestions()
    }, 5000)

    return () => clearInterval(intervalId)
  }, [])

  return (
    /* eslint-disable multiline-ternary */
    <>
      {questions.length > 0
        ? (
          <ul>
            {questions.map((question) =>
              <QuestionPresent
                key={question.id}
                id={question.id}
                likes={question.likes}
                questionText={question.text}
              />
            )}
          </ul>
          ) : (
            <h1 className="u-align-center">{props.title}</h1>
          )}
    </>
    /* eslint-enable multiline-ternary */
  )
}

export default PresentBox
