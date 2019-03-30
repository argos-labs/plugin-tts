#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ai.tts.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from uuid import uuid4
from unittest import TestCase
from argoslabs.ai.tts import _main as main
from tempfile import gettempdir


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_empty_parameter(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_unknown_engine(self):
        try:
            _ = main('unknown', 'hello world?')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_missing_msg(self):
        try:
            _ = main('google')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_say_hello(self):
        try:
            r = main('google', 'Hello world?')
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_say_hello_slow(self):
        try:
            r = main('google', 'Hello slow world?', '--slow')
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0250_say_hello_ko(self):
        try:
            r = main('google', '안녕하세요? 저는 TTS입니다.', '--lang', 'ko')
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0260_say_hello_ja(self):
        try:
            r = main('google', 'こんにちは世界？私はTTSです.', '--lang', 'ja')
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0270_say_hello_zh_cn(self):
        try:
            r = main('google', '你好，世界？我是TTS.', '--lang', 'zh-cn')
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_say_hello_save_mp3(self):
        # write error happen so use temppdir
        mp3f = os.path.join(gettempdir(), '%s.mp3' % uuid4())
        try:
            r = main('google', 'Hello save world?', '--save-mp3', mp3f)
            self.assertTrue(r and os.path.exists(mp3f))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(mp3f):
                os.remove(mp3f)

    # ==========================================================================
    def test0310_say_hello_save_mp3(self):
        # write error happen so use temppdir
        mp3f = os.path.join(gettempdir(), '%s.mp3' % uuid4())
        try:
            r = main('google', 'Hello save world?', '--save-mp3', mp3f)
            self.assertTrue(r and os.path.exists(mp3f))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(mp3f):
                os.remove(mp3f)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
