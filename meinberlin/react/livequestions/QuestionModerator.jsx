import React, { useState, useEffect, useCallback } from 'react'
import django from 'django'
import LikeCard from './LikeCard'
import { classNames } from '../contrib/helpers'

const hiddenText = django.gettext('mark as hidden')
const undoHiddenText = django.gettext('undo mark as hidden')
const doneText = django.gettext('mark as done')
const addLiveText = django.gettext('added to live list')
const removeLiveText = django.gettext('remove from live list')
const addBookmarkText = django.gettext('add bookmark')
const removeBookmarkText = django.gettext('remove bookmark')

const QuestionModerator = ({
  category,
  children,
  displayIsAnswered,
  displayIsHidden,
  displayIsLive,
  displayIsOnShortlist,
  handleLike,
  id,
  is_answered: _isAnswered,
  is_hidden: _isHidden,
  is_live: _isLive,
  is_on_shortlist: _isOnShortlist,
  likes,
  togglePollingPaused,
  updateQuestion
}) => {
  const [isOnShortlist, setisOnShortlist] = useState(_isOnShortlist)
  const [isLive, setIsLive] = useState(_isLive)
  const [isHidden, setIsHidden] = useState(_isHidden)
  const [isAnswered, setIsAnswered] = useState(_isAnswered)
  const [likeCount, setLikeCount] = useState(likes.count)
  const [sessionLike, setSessionLike] = useState(likes.session_like)

  // Copying props to local state ensures instant updates when interacting with the moderator buttons (for example: toggleIsOnShortList)
  // If the props were used directly, there would be a UI delay due to polling in the QuestionBox component.
  useEffect(() => {
    setisOnShortlist(_isOnShortlist)
  }, [_isOnShortlist])

  useEffect(() => {
    setIsLive(_isLive)
  }, [_isLive])

  useEffect(() => {
    setIsHidden(_isHidden)
  }, [_isHidden])

  useEffect(() => {
    setIsAnswered(_isAnswered)
  }, [_isAnswered])

  useEffect(() => {
    setLikeCount(likes.count)
    setSessionLike(likes.session_like)
  }, [likes])

  const toggleIsOnShortList = () => {
    const value = !isOnShortlist
    const boolValue = value ? 1 : 0
    const data = { is_on_shortlist: boolValue }
    updateQuestion(data, id)
      .then((response) => response.json())
      .then(responseData => {
        setisOnShortlist(responseData.is_on_shortlist)
      })
      .then(() => togglePollingPaused())
  }

  const toggleIslive = () => {
    const value = !isLive
    const boolValue = value ? 1 : 0
    const data = { is_live: boolValue }
    updateQuestion(data, id)
      .then((response) => response.json())
      .then(responseData => {
        setIsLive(responseData.is_live)
      })
      .then(() => togglePollingPaused())
  }

  const toggleIsAnswered = () => {
    const value = !isAnswered
    const boolValue = value ? 1 : 0
    const data = { is_answered: boolValue }
    updateQuestion(data, id)
      .then((response) => response.json())
      .then(responseData => {
        setIsAnswered(responseData.is_answered)
      })
      .then(() => togglePollingPaused())
  }

  const toggleIshidden = () => {
    const value = !isHidden
    const boolValue = value ? 1 : 0
    const data = { is_hidden: boolValue }
    updateQuestion(data, id)
      .then((response) => response.json())
      .then(responseData => {
        setIsHidden(responseData.is_hidden)
      })
      .then(() => togglePollingPaused())
  }

  const handleErrors = (response) => {
    if (!response.ok) {
      throw new Error(response.statusText)
    }
    return response
  }

  const handleLikeClick = useCallback(() => {
    const newSessionLike = !sessionLike
    handleLike(id, newSessionLike)
      .then(handleErrors)
      .then(() => {
        setSessionLike(newSessionLike)
        setLikeCount((prevLikes) => prevLikes + (newSessionLike ? 1 : -1))
      })
      .catch((error) => {
        console.log(error.message)
      })
  }, [sessionLike, handleLike, id])

  return (
    <LikeCard
      title={children}
      category={category}
      isOnShortlist={isOnShortlist}
      likes={{
        count: likeCount,
        session_like: sessionLike
      }}
      onLikeClick={handleLikeClick}
    >
      <div className="functions">
        {displayIsHidden && (
          <button
            type="button"
            className={classNames(
              'cardbutton card__button',
              isHidden && 'card__button--active'
            )}
            onClick={toggleIshidden}
            aria-label={isHidden ? undoHiddenText : hiddenText}
            title={isHidden ? undoHiddenText : hiddenText}
          >
            <i
              className={classNames(
                'fas fa-eye',
                isHidden && 'fa-eye-slash'
              )}
              aria-hidden="true"
            />
          </button>
        )}
        {displayIsOnShortlist && (
          <button
            type="button"
            className={classNames(
              'cardbutton card__button',
              isOnShortlist && 'card__button--active'
            )}
            onClick={toggleIsOnShortList}
            aria-label={
              isOnShortlist ? removeBookmarkText : addBookmarkText
            }
            title={
              isOnShortlist ? removeBookmarkText : addBookmarkText
            }
          >
            <i className="fas fa-bookmark" aria-hidden="true" />
          </button>
        )}
        {displayIsAnswered && (
          <button
            type="button"
            className={classNames(
              'cardbutton card__button',
              isAnswered && 'card__button--active'
            )}
            onClick={toggleIsAnswered}
            aria-label={doneText}
            title={doneText}
          >
            <i className="fas fa-check" aria-hidden="true" />
          </button>
        )}
        {displayIsLive && (
          <button
            type="button"
            className={classNames(
              'cardbutton card__button',
              isLive && 'card__button--active'
            )}
            onClick={toggleIslive}
            aria-label={isLive ? removeLiveText : addLiveText}
            title={isLive ? removeLiveText : addLiveText}
          >
            <i className="fas fa-tv" aria-hidden="true" />
          </button>
        )}
      </div>
    </LikeCard>
  )
}

export default QuestionModerator
