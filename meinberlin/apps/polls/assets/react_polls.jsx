import { EditPollQuestions } from './EditPollQuestions'
const React = require('react')
const ReactDOM = require('react-dom')
const { PollQuestions } = require('./PollQuestions')

module.exports.renderPolls = function (element) {
  const pollId = element.getAttribute('data-poll-id')

  ReactDOM.render(<PollQuestions pollId={pollId} />, element)
}

module.exports.renderPollManagement = function (element) {
  const poll = JSON.parse(element.getAttribute('data-poll'))
  const module = element.getAttribute('data-module')

  const reloadOnSuccess = JSON.parse(element.getAttribute('data-reloadOnSuccess'))

  ReactDOM.render(<EditPollQuestions module={module} poll={poll} reloadOnSuccess={reloadOnSuccess} />, element)
}
