# flac-tags

更新 FLAC meta 标签，提供繁简转换，根据标签重命名 flac 文件。

```
Usage: flac-tag.py [OPTIONS] [FILES]...

Options:
  --update-tag / --no-update-tag  convert tag Chinese (S->T)
  --split-artist / --no-split-artist
                                  split artist tag with delimiters ,/;&
  -c, --chinese-convert [none|s2t|t2s]
                                  convert tag Chinese. available values: s2t,
                                  t2s

  --rename                        rename file with format "%artist% - %title%"
  --help                          Show this message and exit.
  ```
