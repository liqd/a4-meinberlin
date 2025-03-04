import django from 'django'

export const notificationsData = {
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
    userRepliedIdeaText: (title) => django.interpolate(
      django.gettext('A user has replied to your idea in %(title)s'),
      { title },
      true
    ),
    moderatorRepliedCommentText: (title) => django.interpolate(
      django.gettext('A moderator has responded to your comment in %(title)s'),
      { title },
      true
    ),
    userRepliedCommentText: (title) => django.interpolate(
      django.gettext('A user has replied to your comment in %(title)s'),
      { title },
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
  searchProfiles: {
    title: django.gettext('Search Profiles'),
    description: django.gettext(
      'Here you will find newly published participation projects that match your search profiles.'
    ),
    descriptionNoItems: django.gettext(
      'No results from your saved searches yet. Add new saved searches and wait for a matching project to be published.'
    ),
    buttonText: django.gettext('Save a search'),
    projectMatchesSearchProfileText: (title, name) => django.interpolate(
      django.gettext('A new project, %(title)s, matches your search profile %(name)s'),
      { title, name },
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
    ),
    offlineEvent: (eventName, title, date) => django.interpolate(
      django.gettext('The event %(eventName)s is coming up for the project %(title)s. It will take place on %(date)s'),
      { eventName, title, date },
      true
    )
  },
  viewIdeaText: django.gettext('View idea'),
  viewCommentText: django.gettext('View comment'),
  viewProjectText: django.gettext('View project')
}

export const notificationSettingsData = [
  {
    header: django.gettext('Project-Related Notifications'),
    notifications: {
      email_newsletter: {
        title: django.gettext('E-Mail Newsletter'),
        description: django.gettext('Receive newsletters with updates and news about the projects you follow via e-mail.')
      },
      notify_followers_phase_started: {
        title: django.gettext('Participation Start'),
        description: django.gettext('Receive a notification when a participation begins in a project you follow.'),
        activityFeedName: 'track_followers_phase_started'
      },
      notify_followers_phase_over_soon: {
        title: django.gettext('Participation End'),
        description: django.gettext('Receive a notification when a participation is near its end in a project you follow.'),
        activityFeedName: 'track_followers_phase_over_soon'
      },
      notify_followers_event_upcoming: {
        title: django.gettext('Event'),
        description: django.gettext('Receive notifications for upcoming events in projects you follow.'),
        activityFeedName: 'track_followers_event_upcoming'
      }
    }
  },
  {
    header: django.gettext('Interactions with Other Users or Moderation'),
    notifications: {
      notify_creator: {
        title: django.gettext('Reactions of other users'),
        description: django.gettext('Receive a notification when someone reacts to your contribution with a comment.')
      },
      notify_creator_on_moderator_feedback: {
        title: django.gettext('Reactions of moderation'),
        description: django.gettext('Receive a notification for feedback and status changes of your idea from the moderation.')
      }
    }
  },
  {
    header: django.gettext('Notifications for Initiators and Moderators'),
    restricted: true,
    notifications: {
      notify_initiators_project_created: {
        title: django.gettext('New Project in Your Organization'),
        description: django.gettext('Receive a notification when a new project is created in your organization.')
      },
      notify_moderator: {
        title: django.gettext('New Contribution in a Moderated Project'),
        description: django.gettext('Receive a notification when a new contribution is added to a project you moderate.')
      }
    }
  }
]
