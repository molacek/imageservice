"""Test module for imageservice"""
from unittest import TestCase

import imageservice


class TestValidate(TestCase):
    def test_existing_image(self):
        t = imageservice.validate(
            "https://img118.imagetwist.com/th/31313/sv5qixhxx9if.jpg"
        )
        self.assertTrue(t == "ok")

    def test_removed_image(self):
        t = imageservice.validate(
            "https://img118.imagetwist.com/th/31279/hk662ayvizp1.jpg"
        )
        self.assertTrue(t == "not_found")

    def test_non_existing_service(self):
        t = imageservice.validate(
            "https://img30.imXagetwist.com/th/27246/33j89k83n00g.jpg"
        )
        self.assertTrue(t == "not_implemented")

    def test_upload_image(self):
        us = imageservice.imagetwist.Imagetwist('gr190501', 'Dopici123!')
        (thumb, img) = us.upload('/home/lukas/Pictures/newstar/Gia/298/'
                                 'Newstar Gia II - Set 298 (1).jpeg')
        print(thumb, img)
        self.assertTrue(True)
