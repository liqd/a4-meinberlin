import pytest

from meinberlin.apps.projects.rules import has_no_participant_contributions


@pytest.fixture
def initiator(organisation, user_factory):
    initiator = user_factory()
    organisation.initiators.add(initiator)
    return initiator


@pytest.fixture
def project(organisation, project_factory):
    return project_factory(organisation=organisation)


@pytest.fixture
def module(project, module_factory):
    return module_factory(project=project)


@pytest.mark.django_db
def test_no_participant_contributions_with_initiators_no_contributions(
    initiator, project
):
    """Test: Project with initiators but without contributions should return True."""
    assert has_no_participant_contributions.test(initiator, project) is True


@pytest.mark.django_db
def test_no_participant_contributions_only_initiator_items(
    initiator, project, module, idea_factory
):
    """Test: Project with only initiator items should return True."""
    idea_factory(module=module, creator=initiator)

    assert has_no_participant_contributions.test(initiator, project) is True


@pytest.mark.django_db
def test_no_participant_contributions_participant_items(
    initiator, project, module, user_factory, idea_factory
):
    """Test: Project with participant items should return False."""
    idea_factory(module=module, creator=user_factory())

    assert has_no_participant_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_participant_contributions_participant_comments(
    initiator, project, module, user_factory, topic_factory, comment_factory
):
    """Test: Project with participant comments should return False."""
    topic = topic_factory(module=module)
    comment_factory(content_object=topic, creator=user_factory())

    assert has_no_participant_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_participant_contributions_only_initiator_comments(
    organisation, project, module, user_factory, topic_factory, comment_factory
):
    """Test: Project with only initiator comments should return True."""
    # Remove automatically created initiators
    organisation.initiators.clear()
    initiator = user_factory()
    organisation.initiators.add(initiator)
    # Topic must also be created by the initiator, as it is an Item
    topic = topic_factory(module=module, creator=initiator)
    comment_factory(content_object=topic, creator=initiator)

    assert has_no_participant_contributions.test(initiator, project) is True


@pytest.mark.django_db
def test_no_participant_contributions_only_group_member_items(
    organisation,
    group_factory,
    project_factory,
    module_factory,
    user_factory,
    idea_factory,
):
    """Test: Contributions only from group members should return True."""
    group = group_factory()
    group_member = user_factory.create(groups=(group,))
    project = project_factory(organisation=organisation, group=group)
    module = module_factory(project=project)
    idea_factory(module=module, creator=group_member)

    assert has_no_participant_contributions.test(group_member, project) is True


@pytest.mark.django_db
def test_no_participant_contributions_other_group_member_items_allowed_for_group_member(
    organisation,
    group_factory,
    project_factory,
    module_factory,
    user_factory,
    idea_factory,
):
    """Test: Content by another group member does not block a group member (AC2)."""
    group = group_factory()
    creator = user_factory.create(groups=(group,))
    deletor = user_factory.create(groups=(group,))
    project = project_factory(organisation=organisation, group=group)
    module = module_factory(project=project)
    idea_factory(module=module, creator=creator)

    assert has_no_participant_contributions.test(deletor, project) is True


@pytest.mark.django_db
def test_no_participant_contributions_other_group_member_items_allowed_for_initiator(
    initiator,
    organisation,
    group_factory,
    project_factory,
    module_factory,
    user_factory,
    idea_factory,
):
    """Test: Content by group members still allowed for the initiator (AC2)."""
    group = group_factory()
    creator = user_factory.create(groups=(group,))
    project = project_factory(organisation=organisation, group=group)
    module = module_factory(project=project)
    idea_factory(module=module, creator=creator)

    assert has_no_participant_contributions.test(initiator, project) is True


@pytest.mark.django_db
def test_no_participant_contributions_non_group_member_items(
    organisation,
    group_factory,
    project_factory,
    module_factory,
    user_factory,
    idea_factory,
):
    """Test: Project with non-group-member items should return False."""
    group = group_factory()
    group_member = user_factory.create(groups=(group,))
    project = project_factory(organisation=organisation, group=group)
    module = module_factory(project=project)
    idea_factory(module=module, creator=user_factory())

    assert has_no_participant_contributions.test(group_member, project) is False


@pytest.mark.django_db
def test_no_participant_contributions_participant_votes(
    initiator,
    project,
    module,
    user_factory,
    poll_factory,
    question_factory,
    choice_factory,
    vote_factory,
):
    """Test: Project with participant votes should return False."""
    poll = poll_factory(module=module)
    question = question_factory(poll=poll, multiple_choice=True)
    choice = choice_factory(question=question)
    vote_factory(choice=choice, creator=user_factory())

    assert has_no_participant_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_participant_contributions_participant_answers(
    initiator,
    project,
    module,
    user_factory,
    poll_factory,
    question_factory,
    answer_factory,
):
    """Test: Project with participant answers should return False."""
    poll = poll_factory(module=module)
    question = question_factory(poll=poll, is_open=True)
    answer_factory(question=question, creator=user_factory())

    assert has_no_participant_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_participant_contributions_participant_ratings(
    initiator,
    project,
    module,
    user_factory,
    idea_factory,
    rating_factory,
):
    """Test: Project with participant ratings should return False."""
    idea = idea_factory(module=module)
    rating_factory(content_object=idea, creator=user_factory(), value=1)

    assert has_no_participant_contributions.test(initiator, project) is False
