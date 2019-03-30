#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ai.tts`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2019/03/08]
#     - starting

################################################################################
import os
import sys
import time
import shutil
from random import randint
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from gtts import gTTS
from tempfile import gettempdir
from playsound import playsound


################################################################################
lang_dict = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en-au': 'English (Australia)',
    'en-ca': 'English (Canada)',
    'en-gb': 'English (UK)',
    'en-gh': 'English (Ghana)',
    'en-ie': 'English (Ireland)',
    'en-in': 'English (India)',
    'en-ng': 'English (Nigeria)',
    'en-nz': 'English (New Zealand)',
    'en-ph': 'English (Philippines)',
    'en-tz': 'English (Tanzania)',
    'en-uk': 'English (UK)',
    'en-us': 'English (US)',
    'en-za': 'English (South Africa)',
    'en': 'English',
    'eo': 'Esperanto',
    'es-es': 'Spanish (Spain)',
    'es-us': 'Spanish (United States)',
    'es': 'Spanish',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr-ca': 'French (Canada)',
    'fr-fr': 'French (France)',
    'fr': 'French',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'km': 'Khmer',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt-br': 'Portuguese (Brazil)',
    'pt-pt': 'Portuguese (Portugal)',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'su': 'Sundanese',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Filipino',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'vi': 'Vietnamese',
    'zh-cn': 'Chinese (Mandarin/China)',
    'zh-tw': 'Chinese (Mandarin/Taiwan)',
}


################################################################################
@func_log
def do_tts(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    mp3file = None
    if argspec.engine == 'google':
        try:
            tts = gTTS(argspec.msg, lang=argspec.lang, slow=argspec.slow)
            mp3file = os.path.join(gettempdir(),
                                   'gtts_%06d.mp3' % randint(1, 999999))
            if os.path.exists(mp3file):
                os.remove(mp3file)
            tts.save(mp3file)
            if not os.path.exists(mp3file):
                raise IOError('Result mp3 file "%s" does not exists.' % mp3file)
            playsound(mp3file)
        finally:
            time.sleep(1)
            if os.path.exists(mp3file):
                if argspec.save_mp3:
                    shutil.move(mp3file, argspec.save_mp3, )
                else:
                    os.remove(mp3file)
    else:
        raise RuntimeError('Not supported TTS engine "%s"' % argspec.engine)
    mcxt.logger.info('>>>end...')
    return True


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='ai',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Text to Speech',
        icon_path=get_icon_path(__file__),
        description='Text to Speech using AI engine (google, ...)',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--save-mp3', '-o',
                          input_method='filewrite',
                          help='mp3 file to save the result of tts')
        mcxt.add_argument('--lang', '-l', default='en',
                          choices=list(lang_dict.keys()),
                          help='language to use (en, es, ko, ja, ...), '
                               'default is "en"')
        mcxt.add_argument('--slow', '-s', action='store_true',
                          help='if set say slow TTS')
        # ##################################### for app dependent parameters
        mcxt.add_argument('engine',
                          choices=['google'],
                          help='TTS engine to use')
        mcxt.add_argument('msg', help='message to TTS')
        argspec = mcxt.parse_args(args)
        return do_tts(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
