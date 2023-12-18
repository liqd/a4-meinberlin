import React from 'react'
import django from 'django'
import {
  MapPopup
} from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MapPopup'

const Ratings = ({ feature }) => (
  <>
    <span className="map-popup-upvotes">
      {feature.properties.positive_rating_count}
      <span className="fa fa-chevron-up" aria-hidden="true" />
    </span>
    <span className="map-popup-downvotes">
      {feature.properties.negative_rating_count}
      <span className="fa fa-chevron-down" aria-hidden="true" />
    </span>
  </>
)

const Support = ({ feature }) => (
  <span className="map-popup-upvotes">
    {feature.properties.positive_rating_count}
    <span className="fa fa-thumbs-up" aria-hidden="true" />
    <span className="aural">{
      django.ngettext(
        'person supports this proposal.',
        'persons support this proposal.',
        feature.properties.positive_rating_count
      )
    }
    </span>
  </span>
)

const VoteCount = ({ feature }) => (
  <span className="map-popup-vote-count">
    {feature.properties.vote_count}
    <span className="fa-regular fa-square-check" aria-hidden="true" />
    <span className="aural">{
      django.ngettext(
        'person voted for this proposal.',
        'persons voted for this proposal.',
        feature.properties.vote_count
      )
    }
    </span>
  </span>
)

const CommentCount = ({ feature }) => (
  <span className="map-popup-comments-count">
    {feature.properties.comments_count}
    <span className="fa fa-comment" aria-hidden="true" />
    <span className="aural">{
      django.ngettext(
        'person commented on this proposal.',
        'persons commented on this proposal.',
        feature.properties.comments_count
      )
    }
    </span>
  </span>
)

/**
 * Renders a popup for an idea feature on a map.
 *
 * @param {Object} props - The component props.
 * @param {Object} props.feature - The geojson feature.
 * @param {boolean} props.hideRatings - Whether to hide the ratings.
 * @param {boolean} props.hideSupport - Whether to hide the support.
 * @param {boolean} props.hideVoteCount - Whether to hide the vote count.
 * @returns {JSX.Element} The JSX element representing the popup.
 */
export const IdeaPopup = ({ feature, hideRatings, hideSupport, hideVoteCount }) => (
  <MapPopup feature={feature}>
    <div className="maps-popups-popup-name">
      <a href={feature.properties.url}>
        {feature.properties.name}
      </a>
    </div>
    <div className="maps-popups-popup-meta">
      {!hideRatings && <Ratings feature={feature} />}
      {!hideSupport && <Support feature={feature} />}
      {!hideVoteCount && <VoteCount feature={feature} />}
      <CommentCount feature={feature} />
    </div>
  </MapPopup>
)
