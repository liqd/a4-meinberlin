import React from 'react'
import django from 'django'
import {
  MapPopup
} from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MapPopup'
import { useFetchedItems } from '../contexts/FetchItemsProvider'

const translations = {
  getVotes: (count) => {
    const countText = django.ngettext('Vote', 'Votes', count)
    return django.interpolate(countText, [count])
  },
  getComments: (count) => {
    const countText = django.ngettext('Comment', 'Comments', count)
    return django.interpolate(countText, [count])
  },
  getLikes: (count) => {
    const countText = django.ngettext('Like', 'Likes', count)
    return django.interpolate(countText, [count])
  },
  getDislikes: (count) => {
    const countText = django.ngettext('Dislike', 'Dislikes', count)
    return django.interpolate(countText, [count])
  },
  support: django.gettext('Support'),
  detailsStr: django.gettext('Item details'),
  toStr: django.gettext('to:')
}

const Ratings = ({ feature }) => (
  <>
    <span className="map-popup-upvotes">
      <strong>{feature.properties.positive_rating_count}</strong>&nbsp;
      {translations.getLikes(feature.properties.positive_rating_count)}
    </span>
    <span className="map-popup-downvotes">
      <strong>{feature.properties.negative_rating_count}</strong>&nbsp;
      {translations.getDislikes(feature.properties.negative_rating_count)}
    </span>
  </>
)

const Support = ({ feature }) => (
  <span className="map-popup-upvotes">
    <strong>{feature.properties.positive_rating_count}</strong> {translations.support}
  </span>
)

// FIXME: This might not be needed anymore, it's not visible in the design
const VoteCount = ({ feature }) => (
  <span className="map-popup-vote-count">
    <strong>{feature.properties.vote_count}</strong>&nbsp;
    {translations.getVotes(feature.properties.vote_count)}
  </span>
)

const CommentCount = ({ feature }) => (
  <span className="map-popup-comments-count">
    <strong>{feature.properties.comment_count}</strong>&nbsp;
    {translations.getComments(feature.properties.comment_count)}
  </span>
)

/**
 * Renders a popup for an item feature on a map.
 *
 * @param {Object} props - The component props.
 * @param {Object} props.feature - The geojson feature.
 * @returns {JSX.Element} The JSX element representing the popup.
 */
export const ItemPopup = ({ feature }) => {
  const fetchedItemsReturn = useFetchedItems()

  const viewRates = fetchedItemsReturn?.results.list?.permissions.view_rate_count
  const viewSupport = fetchedItemsReturn?.results.list?.permissions.view_support_count
  const viewVoteCount = fetchedItemsReturn?.results.list?.permissions.view_vote_count
  return (
    <MapPopup feature={feature}>
      <div className="maps-popups-popup-name">
        <a href={feature.properties.url}>
          {feature.properties.name}
        </a>
      </div>
      <div className="maps-popups-popup-meta">
        {viewRates && <Ratings feature={feature} />}
        {viewSupport && <Support feature={feature} />}
        {viewVoteCount && <VoteCount feature={feature} />}
        <CommentCount feature={feature} />
      </div>
      <a href={feature.properties.url} className="more">{translations.detailsStr}
        <span className="aural">{translations.toStr} {feature.properties.name}</span>
      </a>
    </MapPopup>
  )
}
