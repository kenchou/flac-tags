#!/usr/bin/env python

import click
import mutagen
import opencc
import re

from pathlib import Path


@click.command()
@click.argument('files', nargs=-1)
@click.option('--update-tag/--no-update-tag', is_flag=True, help='convert tag Chinese (S->T)')
@click.option('--split-artist/--no-split-artist', is_flag=True, help='split artist tag with delimiters ,/;&')
@click.option('-c', '--chinese-convert', type=click.Choice(['none', 's2t', 't2s'], case_sensitive=False),
              help='convert tag Chinese. available values: s2t, t2s')
@click.option('--rename', 'rename', is_flag=True, help='rename file with format "%artist% - %title%"')
def fix_tag(files, update_tag, split_artist, chinese_convert, rename):
    cc_cfg = f'{chinese_convert}.json' if chinese_convert else 't2s.json'
    han = opencc.OpenCC(cc_cfg)

    delimiters = re.compile('[,;&/]')
    for filename in files:
        filename = Path(filename)
        ext = filename.suffix
        audio = mutagen.File(filename)
        print(f'\n{filename.name}')
        print('---')
        print(audio.pprint())
        print('---')
        is_updated = False
        for k in audio:
            new_tags = audio[k]
            if isinstance(new_tags, str):
                new_tags = han.convert(new_tags)
            elif isinstance(new_tags, list):
                new_tags = []
                for old_tag in audio[k]:
                    new_tag = old_tag
                    if chinese_convert:
                        new_tag = han.convert(new_tag)
                    if 'ARTIST' == k.upper() and delimiters.search(new_tag):
                        if split_artist:
                            new_tag = [x.strip() for x in delimiters.split(new_tag)]
                        else:
                            click.secho('Detected delimiters in "ARTIST" tag. '
                                        'use --update-tag --split-artist to split artists.',
                                        err=True, fg='yellow')
                    if isinstance(new_tag, str):
                        new_tags.append(new_tag)
                    else:
                        new_tags.extend(new_tag)
            if audio[k] != new_tags:
                click.secho(f'{k}={audio[k]} => {new_tags}', fg='green')
                is_updated = True
                audio[k] = new_tags
        if is_updated:
            audio.pprint()
            if update_tag:
                audio.save()
            else:
                click.secho('set --update-tag to convert tag and update', err=True, fg='yellow')
        if 'TITLE' not in audio:
            click.secho(f'File "{filename}" has not set tags "title" / "artist', err=True, fg='yellow')
            continue
        title = audio['TITLE'][0]
        artists = ', '.join(audio['ARTIST'])
        new_filename = f'{artists} - {title}{ext}'
        if filename.name != new_filename:
            click.secho(f'{filename.name} => {new_filename}', fg='green')
            if rename:
                filename.rename(filename.parent / new_filename)
            else:
                click.secho('set --rename to rename file', err=True, fg='yellow')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fix_tag()
