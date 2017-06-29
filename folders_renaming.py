#! /usr/bin/env python
# -*- coding: mbcs -*-

import os
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
import sys
import re

def find_audio(folder):
    acceptable_formats = {'ID3': ID3, 'M4A': MP4,
                         'fLaC': FLAC, 'MAC': APEv2}
    for filename in folder:
        with open(u'./{}'.format(filename)) as sys.stdin:
            header = sys.stdin.read()[:15]
            for format_key in acceptable_formats.keys():
                if format_key in header:
                    return filename, acceptable_formats[format_key]
    return None, None

def accessing_tags(audio, fileformat):
    album_tags = {FLAC: 'ALBUM', MP4: 'soal', ID3: 'TALB', APEv2: 'Album'}
    artist_tags = {FLAC: 'ARTIST', MP4: 'soar', ID3: 'TPE1', APEv2: 'Artist'}
    date_tags = {FLAC: 'DATE', MP4: '©day', ID3: 'TDRC', APEv2: 'Year'}
      
    _artist = audio[artist_tags[fileformat]][0]
    _album = audio[album_tags[fileformat]][0]
    _date = audio[date_tags[fileformat]][0]
    
    return (_tag for _tag in unicode_checker(_artist, _album, _date))


def unicode_checker(*tags):
    for _tag in tags:
        if not '\u' in _tag.encode('unicode_escape'):
            yield _tag.encode('unicode_escape').decode('string_escape').decode('mbcs')
        else:
            yield _tag
 
def main():
    folders = [name for name in os.listdir(u'.') if os.path.isdir(name)]
    
    for folder in folders:
        rel_dir_path = os.path.join('./', folder).encode('utf8')
        os.chdir(rel_dir_path.decode('utf8'))
        
        main()
        
        folders_content = [name for name in os.listdir(u'.') if not os.path.isdir(name)]
        (filename, fileformat) = find_audio(folders_content)
    
        if fileformat is not None:
            audio = fileformat(u'./{}'.format(filename))
            try:
                (artist, album, date) = accessing_tags(audio, fileformat)
            except KeyError:
                print 'file {} hasnt got all of the requirable tags!'.format(filename.encode('utf8'))
            else:
                print (artist, album, date)
                new_name = u'{} - {} ({})'.format(artist, album, date)
                new_name = re.sub(r'[*|\:"<>?/]', '-', new_name)
                os.chdir('..')
                os.rename(folder, new_name)
                new_path = os.path.join('./', new_name)
                os.chdir(new_path)
                #os.chdir('./{}'.format(new_name.decode('utf8')))
        os.chdir('..')
        #ea = mutagen.File('./{}'.format(os.listdir(".")[0]))

if __name__ == '__main__':
    main()
