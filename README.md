# flac-tags

更新 FLAC meta 标签，提供繁简转换，根据标签重命名 flac 文件。

```
Options:
  --update-tag / --no-update-tag  convert tag Chinese (S->T)
  --split-artist / --no-split-artist
                                  split artist tag with delimiters ,/;&
  -cc, --chinese-convert <TEXT TEXT>...
                                  convert tag Chinese. from, to. eg. -cc tw
                                  cn. available values: st, cn, hk, tw, cnt,
                                  jp
  --rename                        rename file with format "%artist% - %title%"
  --help                          Show this message and exit.  
```
