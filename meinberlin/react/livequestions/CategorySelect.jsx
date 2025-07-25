import django from 'django'
import React, { useEffect } from 'react'

const affiliationStr = django.gettext('Affiliation')
const answeredQuestionsStr = django.gettext('Answered questions will be displayed in the statistics according to the chosen affiliation.')

export const CategorySelect = (props) => {
  useEffect(() => {
    const select = document.getElementById('categorySelect')
    select.addEventListener('change', props.onSelect)
  }, [])

  return (
    <div>
      {Object.keys(props.category_dict).length > 0 &&
        <div className="live_questions__select u-spacer-bottom">
          <label htmlFor="categorySelect">{affiliationStr}*</label>
          <div className="form-hint">
            {answeredQuestionsStr}
          </div>
          <select
            name="categorySelect"
            id="categorySelect"
            className="form-control"
            required="required"
            data-minimum-results-for-search="Infinity"
          >
            <option value="">--------</option>
            {Object.keys(props.category_dict).map((categoryPk, index) => {
              return <option key={index} value={categoryPk}>{props.category_dict[categoryPk]}</option>
            })}
          </select>
        </div>}
    </div>
  )
}
