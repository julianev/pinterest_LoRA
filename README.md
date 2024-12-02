# pinterest_LoRA
Use pinterest images to train a LoRA from your Pins!
Creates a folder containing all of the downloaded images and a metadate file.
The metadata csv file contains each image name and the corresponding image caption.

## Setup
Install requirements.

Change permissions for chromedriver
```chmod +x ./chromedriver```

## Download your images
In [pinterest_scaper.py](pinterest_scraper.py), define a search query, e.g., "wavy pattern".

Or create your own pinterest board with curated images and provide your username and the board name.

You can specify the number of images that should be downloaded.
It is possible to train a LoRA with about 20 images.
The script downloads 50 images by default.

## Clean up metadata
Look into the metadata.csv file in the pinterest_images folder and search for missing or not meaningful captions.
Provide good captions for these files.

In our case, we had to clean up just a few captions, the majority of provided captions were informative.

## Train LoRA
In [train_lora.sh](train_lora.sh), change the DATASET_NAME to the folder name with the downloaded images.
Run the script [train_lora.sh](train_lora.sh).

Test the LoRA by running [test_lora.py](test_lora.py).
Provide different prompts for generating images. The script generates images without and with the LoRA for comparison.

## Results
We searched for images with the query "pattern wavy" and trained a LoRA with these images.

These were our results:

### Query: 
![Without Lora](example_images/)

With LoRA:

Todo: show pictures with and without trained LoRA


# Notes

train_text_to_image_lora_py frpm hugging face diffusers 
https://github.com/huggingface/diffusers/blob/main/examples/text_to_image/train_text_to_image_lora.py