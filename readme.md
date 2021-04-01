# VBnK Decoder

Decodes Gauntlet Dark Legacy PS2 `*.VBK` files. 

## Usage
Place these python files in your extracted AUDIO folder and run "vbnk_decoder.py". You'll see a `out` folder along with folders in that representing the `vbk` file it was stored in. The names are found inside the `VAG` header, so they're as accurate as they can be. If for some reason a name wasn't found in the header, it will be named `unk` followed by a number.

## Structure
```
struct Header {
    char Type[4];
    uint FileInfoSize;
    uint Constant;
    uint Unk3;
    uint FileCount;
};
```
A basic archive file, I'm not sure how you would retrieve the file count, but you can easily just read until you reach the next header or end of file.

## Credits
Some helper functions are from [io_scene_abc](https://github.com/cmbasnett/io_scene_abc), at least for the time being!

Research and development by [Haekb (HeyThereCoffeee)](https://github.com/haekb)