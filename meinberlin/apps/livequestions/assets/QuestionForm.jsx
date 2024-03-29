import django from 'django'
import React from 'react'
import { updateItem } from '../../contrib/assets/helpers.js'
import { CategorySelect } from './CategorySelect'

const askQuestionStr = django.gettext('Here you can ask your question')
const questionStr = django.gettext('Question')
const yourQuestionStr = django.gettext('Your question')
const charsStr = django.gettext(' characters')
const postStr = django.gettext('Post')

export default class QuestionForm extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      question: '',
      selectedCategory: '',
      questionCharCount: 0
    }
  }

  selectCategory (e) {
    this.setState({ selectedCategory: e.target.value })
  }

  handleTextChange (e) {
    this.setState({ question: e.target.value })
    this.setState({ comment: e.target.value, questionCharCount: e.target.value.length })
  }

  getPrivacyPolicyLabelWithLinks () {
    const splittedLabel = this.props.privatePolicyLabel.split('{}')
    const termsOfUseUrl = '/terms-of-use'
    const dataProtectionPolicyUrl = '/datenschutz'

    return (
      <span>
        {splittedLabel[0]}
        <a href={dataProtectionPolicyUrl} target="_blank" rel="noreferrer">{splittedLabel[1]}</a>
        {splittedLabel[2]}
        <a href={termsOfUseUrl} target="_blank" rel="noreferrer">{splittedLabel[3]}</a>
        {splittedLabel[4]}
        <a href={dataProtectionPolicyUrl} target="_blank" rel="noreferrer">{splittedLabel[5]}</a>
        {splittedLabel[6]}
      </span>
    )
  }

  addQuestion (e) {
    e.preventDefault()
    const anchor = document.getElementById('question-list-end')
    const url = this.props.questions_api_url
    const data = {
      text: this.state.question,
      category: this.state.selectedCategory
    }
    updateItem(data, url, 'POST')
    this.setState({
      question: '',
      questionCharCount: 0
    })
    anchor.scrollIntoView({ behavior: 'smooth', block: 'end' })
    this.props.restartPolling()
  }

  render () {
    return (
      <form id="id-comment-form" action="" onSubmit={this.addQuestion.bind(this)}>
        <h2>{askQuestionStr}</h2>
        {Object.keys(this.props.category_dict).length > 0
          ? <CategorySelect
              onSelect={this.selectCategory.bind(this)}
              category_dict={this.props.category_dict}
            />
          : ''}
        <label htmlFor="questionTextField">{questionStr}*</label>
        <textarea
          placeholder={yourQuestionStr}
          id="questionTextField"
          className="form-control"
          name="questionTextFieldName"
          rows="3"
          onChange={this.handleTextChange.bind(this)}
          required="required"
          value={this.state.question}
          maxLength="1000"
        />
        <label htmlFor="id-comment-form" className="live_questions__char-count">{this.state.questionCharCount}/1000{charsStr}</label>

        <div className="form-check">
          <label className="form-check__label">
            <input type="checkbox" name="data_protection" id="data_protection_check" required="required" />
            {this.getPrivacyPolicyLabelWithLinks()}
          </label>
        </div>
        <input type="submit" value={postStr} className="submit-button" />
      </form>
    )
  }
}
