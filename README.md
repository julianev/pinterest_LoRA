# pinterest_LoRA

Use pinterest images to train a LoRA from your Pins!
Creates a folder containing all of the downloaded images and a metadate file.
The metadata csv file contains each image name and the corresponding image caption.

## Setup
Change permissions for chromedriver
```chmod +x ./chromedriver```

## Download your images
Define a search query, e.g., "abstract patterns".
Or create your own pinterest board with curated images and provide your username and the board name.
You can specify the number of images that should be downloaded.
It is possible to train a LoRA with about 20 images.
The default number is 50 images.

## Clean up metadata
Look into the metadata.csv file and search for missing or not meaningful captions.
Provide good captions for these files.

In our case, we had to clean up just a few captions, the majority of provided captions were informative.

## Results
We searched for images with the query "pattern wavy" and trained a LoRA with these images.

These were our results:

### Query: 
Without LoRA:

With LoRA:

Todo: show pictures with and without trained LoRA