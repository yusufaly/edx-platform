"""
Add receivers for django signals, and feed data into the monitoring system.

If a model has a class attribute 'METRIC_TAGS' that is a list of strings,
those fields will be retrieved from the model instance, and added as tags to
the recorded metrics.
"""


from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from dogapi import dog_stats_api


def _database_tags(sender, **kwargs):
    """
    Return a tags for the sender and database used in django.db.models signals.
    """
    tags = _model_tags(kwargs, 'instance')

    if 'using' in kwargs:
        tags.append('database:{}'.format(kwargs['using']))

    return tags


def _model_tags(kwargs, key):
    """
    Return a list of all tags for all attributes in kwargs[key].MODEL_TAGS,
    plus a tag for the model class.
    """
    if key not in kwargs:
        return []

    instance = kwargs[key]
    tags = [
        u'{}.{}:{}'.format(key, attr, getattr(instance, attr))
        for attr in getattr(instance, 'MODEL_TAGS', [])
    ]
    tags.append(u'{}.class'.format(instance.__class__.__name__))
    return tags


@receiver(post_save, dispatch_uid='edxapp.monitoring.post_save_metrics')
def post_save_metrics(sender, **kwargs):
    tags = _database_tags(sender, **kwargs)

    if kwargs.pop('created', False):
        dog_stats_api.increment('edxapp.db.model.created', tags=tags)
    else:
        dog_stats_api.increment('edxapp.db.model.updated', tags=tags)


@receiver(post_delete, dispatch_uid='edxapp.monitoring.post_delete_metrics')
def post_delete_metrics(sender, **kwargs):
    tags = _database_tags(sender, **kwargs)

    dog_stats_api.increment('edxapp.db.model.deleted', tags=tags)


@receiver(m2m_changed, dispatch_uid='edxapp.monitoring.m2m_changed_metrics')
def m2m_changed_metrics(sender, **kwargs):
    if 'action' not in kwargs:
        return

    tags = _database_tags(sender, **kwargs)
    tags.extend(_model_tags(kwargs, 'model'))

    action = kwargs['action']

    if action == 'post_add':
        dog_stats_api.increment(
            'edxapp.db.model.m2m.added',
            value=len(kwargs.get('pk_set', [])),
            tags=tags
        )
    elif action == 'post_remove':
        dog_stats_api.increment(
            'edxapp.db.model.m2m.removed',
            value=len(kwargs.get('pk_set', [])),
            tags=tags
        )
    elif action == 'post_clear':
        dog_stats_api.increment(
            'edxapp.db.model.m2m.cleared',
            tags=tags
        )
