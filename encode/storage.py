# Copyright Collab 2015-2016
# See LICENSE for details.

"""
Storage.
"""

from __future__ import unicode_literals

from queued_storage.backends import QueuedStorage

from encode.conf import settings

from django.utils.deconstruct import deconstructible

@deconstructible
class QueuedEncodeSystemStorage(QueuedStorage):
    def __init__(self,
                local=settings.ENCODE_LOCAL_FILE_STORAGE,
                remote=settings.ENCODE_REMOTE_FILE_STORAGE,
                local_options=settings.ENCODE_LOCAL_STORAGE_OPTIONS,
                remote_options=settings.ENCODE_REMOTE_STORAGE_OPTIONS,
                delayed=True,
                *args, **kwargs):
        super(QueuedEncodeSystemStorage, self).__init__(
            local=local,
            remote=remote,
            local_options=local_options,
            remote_options=remote_options,
            delayed=delayed,
            *args, **kwargs)

    def __eq__(self, other):
        return self.foo == other.foo
