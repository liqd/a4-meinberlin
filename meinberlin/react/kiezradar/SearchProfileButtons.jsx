import React from 'react'
import django from 'django'

const renameText = django.gettext('Rename')
const deleteText = django.gettext('Remove')

export default function SearchProfileButtons ({ onEdit, onDelete, loading }) {
  return (
    <div className="search-profile__buttons">
      <button className="search-profile__button" onClick={onEdit}>
        <i className="fa-solid fa-pencil mr-1" />
        {renameText}
      </button>
      <button
        className="search-profile__button"
        onClick={onDelete}
        disabled={loading}
      >
        <i className="fa-classic fa-regular fa-trash-can mr-1" />
        {deleteText}
      </button>
    </div>
  )
}
