# Copyright Collab 2014-2016
# See LICENSE for details.

"""
Tests for the :py:mod:`encode.models` module.
"""

from __future__ import unicode_literals

from django.core.files.base import ContentFile

from encode.models import Audio, Video, EncodingProfile, Encoder
from encode.tests.helpers import WEBM_DATA, FileTestCase

from django.core.files.uploadedfile import SimpleUploadedFile

import encode

import os

from django.conf import settings

from django.contrib.auth.models import User

class MediaBaseTestCase(FileTestCase):
    """
    Tests for the :py:class:`encode.models.MediaBase` model.
    """
    def test_get_media(self):
        """
        `get_media` returns an instance of the model.
        """
        afile = Audio.objects.create(title='Foo')

        self.assertEqual(repr(afile.get_media()), '<Audio: Foo>')

    def test_badProfileIds(self):
        """
        Passing non-existent encoding profile id's to `save()`
        raises an error.
        """
        title = 'test.webm'
        vfile = Video.objects.create(title='Foo')

        # attach file to model
        data = ContentFile(WEBM_DATA, title)

        # store file data but don't save related model until
        # the encoding profiles are saved as well
        getattr(vfile, 'input_file').save(title, data, save=False)

        self.assertRaises(EncodingProfile.DoesNotExist, vfile.save,
            profiles=[18])

    def test_extract_attr(self):
        """
        `is_extract` returns value
        """
        afile = Audio.objects.create(title='Foo')
        afile.extract = True

        afile2 = Video.objects.create(title='Foo2')

        self.assertEqual(afile.extract, True)
        self.assertEqual(afile2.extract, False)


    def test_reference_foreignkey(self):

        user = User()
        user.save()

        afile = Audio.objects.create(title='Foo')
        afile.reference = user
        afile.save()

        self.assertEqual(afile.reference, user)

    def test_extract_length(self):

        def extract_length_cond(seconds):
            if seconds > 60:
                return seconds
            else:
                return 10

        settings.ENCODE_EXTRACT_ACTIVE = True

        settings.ENCODE_EXTRACT_CONDITION = extract_length_cond

        audio = Audio(input_file=SimpleUploadedFile( "audio-short.mp3", open( os.path.dirname(os.path.realpath(__file__)) + "/datas/audio-short.mp3", 'rb').read(),'audio/mpeg'),)
        audio.save()

        audio2 = Audio(input_file=SimpleUploadedFile( "audio-mini.wav", open( os.path.dirname(os.path.realpath(__file__)) + "/datas/audio-mini.wav", 'rb').read(),'audio/wav'),)
        audio2.save()

        self.assertEqual(audio.extract_duration, audio.duration)
        self.assertEqual(audio2.extract_duration, 10)

    def test_extract_length_when_disabled(self):

        def extract_length_cond(seconds):
            if seconds > 60:
                return seconds
            else:
                return 10

        settings.ENCODE_EXTRACT_ACTIVE = False

        settings.ENCODE_EXTRACT_CONDITION = extract_length_cond

        audio = Audio(input_file=SimpleUploadedFile( "audio-short.mp3", open( os.path.dirname(os.path.realpath(__file__)) + "/datas/audio-short.mp3", 'rb').read(),'audio/mpeg'),)
        audio.save()

        audio2 = Audio(input_file=SimpleUploadedFile( "audio-mini.wav", open( os.path.dirname(os.path.realpath(__file__)) + "/datas/audio-mini.wav", 'rb').read(),'audio/wav'),)
        audio2.save()

        self.assertEqual(audio.extract_duration, None)
        self.assertEqual(audio2.extract_duration, None)

