# Word map
![Image of World](https://raw.githubusercontent.com/marcellox98/word_map/master/word_image.jpg)

## Usage
Download the map on github and run:
```
python3 main.py
```

## Add your own data

Create a json file. data sould be structured like this:

```JavaScript
{
  "_index": 2, # the lowest number appears on top
  "_config": [{ # every new item adds a line
   " _name": "Languages", # title of data item (can be empty)
    "language": "Speaks: %s", # [variable name] : [formatting]
    "speaksEN": "Speaks english: %s" # you can add as many variables as you like
  }],
  "NL": {    # Country code
    "language": "Dutch", # variables you put in the config file
   "speaksEN": "yes"
  }
}
```

after creating your datafile you can add it in the countryData map
