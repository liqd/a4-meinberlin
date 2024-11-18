import React from 'react'
import django from 'django'
import LikeCard from './LikeCard'
import { classNames } from '../contrib/helpers'

export default class QuestionModerator extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      is_on_shortlist: this.props.is_on_shortlist,
      is_live: this.props.is_live,
      likes: this.props.likes.count,
      session_like: this.props.likes.session_like,
      is_hidden: this.props.is_hidden,
      is_answered: this.props.is_answered
    }
  }

  toggleIsOnShortList () {
    const value = !this.state.is_on_shortlist
    const boolValue = (value) ? 1 : 0
    const data = { is_on_shortlist: boolValue }
    this.props.updateQuestion(data, this.props.id)
      .then((response) => response.json())
      .then(responseData => this.setState(
        {
          is_on_shortlist: responseData.is_on_shortlist
        }
      ))
      .then(() => this.props.togglePollingPaused())
  }

  toggleIslive () {
    const value = !this.state.is_live
    const boolValue = (value) ? 1 : 0
    const data = { is_live: boolValue }
    this.props.updateQuestion(data, this.props.id)
      .then((response) => response.json())
      .then(responseData => this.setState(
        {
          is_live: responseData.is_live
        }
      ))
      .then(() => this.props.togglePollingPaused())
  }

  toggleIsAnswered () {
    const value = !this.state.is_answered
    const boolValue = (value) ? 1 : 0
    const data = { is_answered: boolValue }
    this.props.removeFromList(this.props.id, data)
  }

  toggleIshidden () {
    const value = !this.state.is_hidden
    const boolValue = (value) ? 1 : 0
    const data = { is_hidden: boolValue }
    this.props.updateQuestion(data, this.props.id)
      .then((response) => response.json())
      .then(responseData => this.setState(
        {
          is_hidden: responseData.is_hidden
        }
      ))
      .then(() => this.props.togglePollingPaused())
  }

  componentDidUpdate (prevProps) {
    if (this.props.is_on_shortlist !== prevProps.is_on_shortlist) {
      this.setState({
        is_on_shortlist: this.props.is_on_shortlist
      })
    }
    if (this.props.is_live !== prevProps.is_live) {
      this.setState({
        is_live: this.props.is_live
      })
    }
    if (this.props.is_hidden !== prevProps.is_hidden) {
      this.setState({
        is_hidden: this.props.is_hidden
      })
    }
    if (this.props.is_answered !== prevProps.is_answered) {
      this.setState({
        is_answered: this.props.is_answered
      })
    }
    if (this.props.likes !== prevProps.likes) {
      this.setState({
        likes: this.props.likes.count,
        session_like: this.props.likes.session_like
      })
    }
  }

  render () {
    const hiddenText = django.gettext('mark as hidden')
    const undoHiddenText = django.gettext('undo mark as hidden')
    const doneText = django.gettext('mark as done')
    const addLiveText = django.gettext('added to live list')
    const removeLiveText = django.gettext('remove from live list')
    const addShortlistText = django.gettext('added to shortlist')
    const removeShortlistText = django.gettext('remove from shortlist')

    return (
      <>
        <LikeCard
          title={this.props.children}
          category={this.props.category}
          isOnShortlist={this.state.is_on_shortlist}
          likes={{
            count: this.state.likes,
            session_like: this.state.session_like
          }}
        >
          <div className="functions">
            {this.props.displayIsHidden && (
              <button
                type="button"
                className={classNames(
                  'cardbutton card__button card__button--hidden',
                  this.state.is_hidden && 'card__button--active'
                )}
                onClick={this.toggleIshidden.bind(this)}
                aria-label={this.props.is_hidden ? hiddenText : undoHiddenText}
                title={this.props.is_hidden ? hiddenText : undoHiddenText}
              >
                <i
                  className={classNames(
                    'fas fa-eye',
                    this.state.is_hidden && 'fa-eye-slash'
                  )}
                  aria-hidden="true"
                />
              </button>
            )}
            {this.props.displayIsOnShortlist && (
              <button
                type="button"
                className={classNames(
                  'cardbutton card__button card__button--shortlist',
                  this.state.is_on_shortlist && 'card__button--active'
                )}
                onClick={this.toggleIsOnShortList.bind(this)}
                aria-label={
                  this.state.is_on_shortlist ? addShortlistText : removeShortlistText
                }
                title={
                  this.state.is_on_shortlist ? addShortlistText : removeShortlistText
                }
              >
                <i className="fas fa-bookmark" aria-hidden="true" />
              </button>
            )}
            {this.props.displayIsAnswered && (
              <button
                type="button"
                className={classNames(
                  'cardbutton card__button card__button--answered',
                  this.props.is_answered && 'card__button--active'
                )}
                onClick={this.toggleIsAnswered.bind(this)}
                aria-label={doneText}
                title={doneText}
              >
                <i className="fas fa-check" aria-hidden="true" />
              </button>
            )}
            {this.props.displayIsLive && (
              <button
                type="button"
                className={classNames(
                  'cardbutton card__button card__button--live',
                  this.state.is_live && 'card__button--active'
                )}
                onClick={this.toggleIslive.bind(this)}
                aria-label={this.state.is_live ? addLiveText : removeLiveText}
                title={this.state.is_live ? addLiveText : removeLiveText}
              >
                <i className="fas fa-tv" aria-hidden="true" />
              </button>
            )}
          </div>
        </LikeCard>
      </>
    )
  }
}
