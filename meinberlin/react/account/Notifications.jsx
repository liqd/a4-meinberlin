import React from 'react'
import django from 'django'
import FeedItem from './FeedItem'
import FeedList from './FeedList'

const translations = {
  interactions: {
    title: django.gettext('Interactions'),
    description: django.gettext(
      'Here you can see all the interactions you have with other users on meinBerlin.'
    ),
    descriptionNoItems: django.gettext(
      'No reactions to your posts yet. Get involved to get reactions.'
    ),
    buttonText: django.gettext('Find participation projects'),
    moderatorReplieIdeaText: (title) => django.interpolate(
      django.gettext('A moderator has responded to your idea in %(title)s'),
      { title },
      true
    ),
    userRepliedIdeaText: (name, title) => django.interpolate(
      django.gettext('%(name)s has replied to your idea in %(title)s'),
      { name, title },
      true
    ),
    moderatorRepliedCommentText: (title) => django.interpolate(
      django.gettext('A moderator has responded to your comment in %(title)s'),
      { title },
      true
    ),
    userRepliedCommentText: (name, title) => django.interpolate(
      django.gettext('%(name)s has replied to your comment in %(title)s'),
      { name, title },
      true
    ),
    userRatedIdeaText: (title) => django.interpolate(
      django.gettext('A user has rated your idea in %(title)s'),
      { title },
      true
    ),
    userRatedCommentText: (title) => django.interpolate(
      django.gettext('A user has rated your comment in %(title)s'),
      { title },
      true
    )
  },
  followedProjects: {
    title: django.gettext('Followed projects'),
    description: django.gettext(
      'Here you will receive all the latest news about the projects you follow.'
    ),
    descriptionNoItems: django.gettext(
      'No followed projects. Find projects to follow them.'
    ),
    buttonText: django.gettext('Find projects'),
    phaseStartedText: (title, date) => django.interpolate(
      django.gettext('%(title)s is now open for participation. You can participate until %(date)s'),
      { title, date },
      true
    ),
    phaseEndedText: (title, date) => django.interpolate(
      django.gettext('%(title)s will end soon. You can still participate until %(date)s'),
      { title, date },
      true
    )
  },
  viewIdeaText: django.gettext('View idea'),
  viewCommentText: django.gettext('View comment'),
  viewProjectText: django.gettext('View project')
}

export default function Notifications ({ interactionsApiUrl, followedProjectsApiUrl, planListUrl }) {
  return (
    <>
      <InteractionsFeed apiUrl={interactionsApiUrl} planListUrl={planListUrl} />
      <FollowedProjectsFeed apiUrl={followedProjectsApiUrl} planListUrl={planListUrl} />
    </>
  )
}

function InteractionsFeed ({ apiUrl, planListUrl }) {
  return (
    <FeedList
      {...translations.interactions}
      apiUrl={apiUrl}
      link={planListUrl}
      renderFeedItem={({ read, action }, index) => {
        const { type, timestamp, link, ...rest } = action
        const text = getInteractionText({ type, ...rest })

        if (!text) {
          return null
        }

        const { title, body, linkText } = text

        return (
          <FeedItem
            key={timestamp + index}
            icon={type === 'comment' ? 'comment' : 'clock'}
            title={title}
            body={body}
            link={link}
            linkText={linkText}
            isRead={read}
            timestamp={timestamp}
          />
        )
      }}
    />
  )
}

function FollowedProjectsFeed ({ apiUrl, planListUrl }) {
  return (
    <FeedList
      {...translations.followedProjects}
      apiUrl={apiUrl}
      link={planListUrl}
      renderFeedItem={({ read, action }, index) => {
        const { type, timestamp, link, ...rest } = action
        const text = getFollowedProjectsText({ type, ...rest })

        if (!text) {
          return null
        }

        const { title, body, linkText } = text

        return (
          <FeedItem
            key={timestamp + index}
            icon="clock"
            title={title}
            body={body}
            link={link}
            linkText={linkText}
            isRead={read}
            timestamp={timestamp}
          />
        )
      }}
    />
  )
}

function getInteractionText (action) {
  const { type, source, body, actor, project } = action

  switch (type) {
    case 'comment':
      switch (source) {
        case 'idea':
        case 'mapidea':
          if (actor.is_moderator) {
            return {
              title: translations.interactions.moderatorReplieIdeaText(project.title),
              body,
              linkText: translations.viewCommentText
            }
          }

          return {
            title: translations.interactions.userRepliedIdeaText(actor.username, project.title),
            body,
            linkText: translations.viewCommentText
          }

        case 'comment':
          if (actor.is_moderator) {
            return {
              title: translations.interactions.moderatorRepliedCommentText(project.title),
              body,
              linkText: translations.viewCommentText
            }
          }

          return {
            title: translations.interactions.userRepliedCommentText(actor.username, project.title),
            body,
            linkText: translations.viewCommentText
          }
      }
      break

    case 'rating':
      switch (source) {
        case 'idea':
        case 'mapidea':
          return {
            title: translations.interactions.userRatedIdeaText(project.title),
            linkText: translations.viewIdeaText
          }

        case 'comment':
          return {
            title: translations.interactions.userRatedCommentText(project.title),
            body,
            linkText: translations.viewCommentText
          }
      }
  }
}

function getFollowedProjectsText (action) {
  const { type, project } = action
  const date = new Date(project.active_phase[2])

  switch (type) {
    case 'phase_started':
      return {
        title: translations.followedProjects.phaseStartedText(project.title, date.toLocaleDateString()),
        linkText: translations.viewProjectText
      }

    case 'phase_soon_over':
      return {
        title: translations.followedProjects.phaseEndedText(project.title, date.toLocaleDateString()),
        linkText: translations.viewProjectText
      }
  }
}
