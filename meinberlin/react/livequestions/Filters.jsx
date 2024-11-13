import React, { useState } from 'react'
import django from 'django'

const allTag = django.gettext('all')
const onlyShowMarkedText = django.gettext('only show marked questions')
const displayNotHiddenText = django.gettext('display only questions which are not hidden')
const orderLikesText = django.gettext('order by likes')
const questionsText = django.gettext('Questions')
const filterText = django.gettext('Filter')
const affiliationText = django.gettext('Affiliation')

const Filter = ({
  categories,
  isModerator,
  displayOnShortlist,
  toggleDisplayOnShortlist,
  displayNotHiddenOnly,
  toggledisplayNotHiddenOnly,
  orderedByLikes,
  toggleOrdering,
  setCategories
}) => {
  const [category, setCategory] = useState(null)

  const selectCategory = (e) => {
    e.preventDefault()
    setCategory(e.target.value)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (category) {
      setCategories(category)
    }
  }

  return (
    <>
      <h2 id="filter-form-heading">{questionsText}</h2>
      <form className="form panel--heavy" onSubmit={handleSubmit} aria-labelledby="filter-form-heading">
        {categories.length > 0 && (
          <div className="form-group">
            <label htmlFor="filterCategorySelect">{affiliationText}*</label>
            <select
              id="filterCategorySelect"
              className="form-control"
              onChange={selectCategory}
            >
              <option value={-1}>{allTag}</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>
        )}
        <div className="form-actions">
          <div className="form-actions__right">
            <button type="submit" className="button">{filterText}</button>
          </div>
        </div>
      </form>
      {isModerator && (
        <div className="block">
          <div className="checkbox-btn u-spacer-right">
            <label
              htmlFor="markedCheck"
              className={'btn switch--btn' + (displayOnShortlist ? ' active' : '')}
              title={onlyShowMarkedText}
            >
              <input
                className="radio__input"
                type="checkbox"
                id="markedCheck"
                name="markedCheck"
                checked={displayOnShortlist}
                onChange={toggleDisplayOnShortlist}
              />
              <span className="visually-hidden">{onlyShowMarkedText}</span>
              <i className="far fa-list-alt" aria-hidden="true" />
            </label>
          </div>
          <div className="checkbox-btn u-spacer-right">
            <label
              htmlFor="displayNotHiddenOnly"
              className={'btn switch--btn' + (displayNotHiddenOnly ? ' active' : '')}
              title={displayNotHiddenText}
            >
              <input
                className="radio__input"
                type="checkbox"
                id="displayNotHiddenOnly"
                name="displayNotHiddenOnly"
                checked={displayNotHiddenOnly}
                onChange={toggledisplayNotHiddenOnly}
              />
              <span className="visually-hidden">{displayNotHiddenText}</span>
              <i className="far fa-eye" aria-hidden="true" />
            </label>
          </div>
          <div className="checkbox-btn">
            <label
              htmlFor="orderedByLikes"
              className={'btn switch--btn' + (orderedByLikes ? ' active' : '')}
              title={orderLikesText}
            >
              <input
                className="radio__input"
                type="checkbox"
                id="orderedByLikes"
                name="orderedByLikes"
                checked={orderedByLikes}
                onChange={toggleOrdering}
              />
              <span className="visually-hidden">{orderLikesText}</span>
              <i className="far fa-thumbs-up" aria-hidden="true" />
            </label>
          </div>
        </div>
      )}
    </>
  )
}

export default Filter
