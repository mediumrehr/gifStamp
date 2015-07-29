# gifStamp

gifStamp is a python script for creating animated gifs from images based on the EXIF data timestamp. gifStamp should be placed in the same directory as the collection of jpg images that this script should be used with.

## Command Format
```sh
python gifStamp.py [[[time_delta] dither] gif_name]
```
### Examples
```sh
$ python gifStamp.py
$ python gifStamp.py 15
$ python gifStamp.py 15 20
$ python gifStamp.py 15 20 myGif
```

## Dependencies
- [ExifRead 2.1.1](https://pypi.python.org/pypi/ExifRead/2.1.1)
- [images2gif 1.0.1](https://pypi.python.org/pypi/images2gif)
- [PILLOW 2.9.0](https://pypi.python.org/pypi/Pillow/2.9.0)

### How to install dependencies
Use pip to install package
```sh
$ pip install <package>
```

### images2gif PILLOW fix
If you get the globalPalette error:
```
"images2gif.py", line 436, in writeGifToFile
  fp.write(globalPalette)
TypeError: must be string or buffer, not None
```
In images2gif.py change line 200:
```
for im in images:
    palettes.append( getheader(im)[1] )
```
to
```
for im in images:
    palettes.append(im.palette.getdata()[1])
```

[via chappy](http://stackoverflow.com/questions/19149643/error-in-images2gif-py-with-globalpalette/22947758#22947758)

## License
Beerware. Feel free to use it, with or without attribution, in your own projects. If you find it helpful, buy me a beer next time you see me at the local pub.
