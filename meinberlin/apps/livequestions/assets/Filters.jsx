import React from 'react'
import django from 'django'

export default class Filter extends React.Component {
  selectCategory (e) {
    e.preventDefault()
    const category = e.target.getAttribute('data-value')
    this.props.setCategories(category)
  }

  getButtonClass () {
    if (this.props.currentCategory === '-1') {
      return 'btn btn--light btn--select live_questions__filters--dropdown dropdown-toggle'
    } else {
      return 'btn btn--light btn--select live_questions__filters--dropdown dropdown-toggle'
    }
  }

  render () {
    const allTag = django.gettext('all')
    const onlyShowMarkedText = django.gettext('only show marked questions')
    const displayNotHiddenText = django.gettext('display only questions which are not hidden')
    const orderLikesText = django.gettext('order by likes')
    return (
      <div className="live_questions__filters">
        <div className="dropdown">
          <button
            className={this.getButtonClass()} type="button" id="dropdownMenuButton"
            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
          >
            {this.props.currentCategoryName}
            <i className="fa fa-caret-down" aria-label={onlyShowMarkedText} />
          </button>
          <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <button className="dropdown-item" data-value={-1} onClick={this.selectCategory.bind(this)} href="#">{allTag}</button>
            {this.props.categories.map((category, index) => {
              return <button className="dropdown-item" key={index} data-value={category} onClick={this.selectCategory.bind(this)} href="#">{category}</button>
            })}
          </div>
        </div>
        {this.props.isModerator &&
          <div className="live_questions__filters--btns">
            <div className="checkbox-btn u-spacer-right">
              <label htmlFor="markedCheck" className="checkbox-btn__label--primary" title={onlyShowMarkedText}>
                <input
                  className="checkbox-btn__input"
                  type="checkbox"
                  id="markedCheck"
                  name="markedCheck"
                  checked={this.props.displayOnShortlist}
                  onChange={this.props.toggleDisplayOnShortlist} // eslint-disable-line react/jsx-handler-names
                />
                <div className="checkbox-btn__text">
                  <i className="far fa-list-alt" aria-label={onlyShowMarkedText} />
                </div>
              </label>
            </div>
            <div className="checkbox-btn u-spacer-right">
              <label htmlFor="displayNotHiddenOnly" className="checkbox-btn__label--primary" title={displayNotHiddenText}>
                <input
                  className="checkbox-btn__input"
                  type="checkbox"
                  id="displayNotHiddenOnly"
                  name="displayNotHiddenOnly"
                  checked={this.props.displayNotHiddenOnly}
                  onChange={this.props.toggledisplayNotHiddenOnly} // eslint-disable-line react/jsx-handler-names
                />
                <span className="checkbox-btn__text">
                  <i className="far fa-eye" aria-label={displayNotHiddenText} />
                </span>
              </label>
            </div>
            <div className="checkbox-btn">
              <label htmlFor="orderedByLikes" className="checkbox-btn__label--primary" title={orderLikesText}>
                <input
                  className="checkbox-btn__input"
                  type="checkbox"
                  id="orderedByLikes"
                  name="orderedByLikes"
                  checked={this.props.orderedByLikes}
                  onChange={this.props.toggleOrdering} // eslint-disable-line react/jsx-handler-names
                />
                <span className="checkbox-btn__text">
                  <i className="far fa-thumbs-up" aria-label={orderLikesText} />
                </span>
              </label>
            </div>
          </div>}
      </div>
    )
  }
}
