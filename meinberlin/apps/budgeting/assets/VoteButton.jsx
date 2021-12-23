import React from 'react'
import django from 'django'
import { useApi } from '../../contrib/assets/ApiProvider'

export const VoteButton = props => {
  const api = useApi()

  const addVote = async () => {
    const data = {
      object_id: props.objectID
    }
    await api.post(props.tokenvoteApiUrl, data)
  }

  const deleteVote = async () => {
    const url = props.tokenvoteApiUrl + props.objectID + '/'
    await api.remove(url)
  }

  const triggerRender = () => {
    // FIXME: distuingishes between if
    // it has a parent that handles onVoteChange
    // or if it is used as widget, and therefore page
    // has to be reloaded --> fix would be one asynchronous way
    if (props.asWidget) {
      window.location.reload()
    } else {
      props.onVoteChange(props.currentPage)
    }
  }

  const handleOnChange = async () => {
    if (props.isChecked) {
      await deleteVote()
    } else {
      await addVote()
    }
    triggerRender()
  }

  const checkedText = django.gettext('Voted')
  const uncheckedText = django.gettext('Give my vote')
  const checkedClass = 'btn btn--full'
  const uncheckedClass = 'btn btn--full btn--light'

  return (
    <div>
      <label
        htmlFor={props.objectID}
        className={props.isChecked ? checkedClass : uncheckedClass}
      >
        <input
          id={props.objectID}
          className="checkbox-btn__input"
          type="checkbox"
          disabled={props.disabled}
          checked={props.isChecked}
          onChange={e => handleOnChange(e)}
        />
        <span>{props.isChecked ? checkedText : uncheckedText}</span>
      </label>
    </div>
  )
}
