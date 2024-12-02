export DATASET_NAME="./pinterest_images_wavy_pattern"
export OUTPUT_DIR="./train_lora/pinterest_lora"
export HUB_MODEL_ID="pinterest_lora"
export MODEL_NAME="runwayml/stable-diffusion-v1-5"

mkdir -p $OUTPUT_DIR

accelerate launch --mixed_precision="bf16"  train_text_to_image_lora.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --dataset_name=$DATASET_NAME \
  --dataloader_num_workers=8 \
  --resolution=512 \
  --center_crop \
  --random_flip \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --max_train_steps=15000 \
  --learning_rate=1e-04 \
  --max_grad_norm=1 \
  --lr_scheduler="cosine" \
  --lr_warmup_steps=0 \
  --output_dir=${OUTPUT_DIR} \
  --checkpointing_steps=500 \
  --caption_column="caption" \
  --validation_prompt="An abstract pattern with wavy lines" \
  --seed=1337