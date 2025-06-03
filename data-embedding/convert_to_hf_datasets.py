import os
from datasets import load_dataset
from huggingface_hub import login, HfApi

# ========================
# Configuration
# ========================
folder_path = "/workspaces/code-space-blank-repo/data-embedding/md"  # Update this path
save_path = "./hf_dataset"             # Where to save locally
push_to_hub = True                    # Set to True if you want to upload
repo_name = "rajivmehtapy/md_highland_ds"  # Your HF repo name

# ========================
# Step 1: Load all .md files into a Dataset
# ========================
print("Loading .md files...")
dataset = load_dataset("text", data_files=os.path.join(folder_path, "*.md"))

# ========================
# Step 2: Add filename metadata (Optional)
# ========================
print("Adding filenames...")

# Get sorted list of files before mapping
folder_path = 'md'  # Update to correct relative path
filenames = sorted(os.listdir(folder_path))

# Modified add_metadata function
def add_metadata(example, idx):
    example['filename'] = filenames[idx % len(filenames)]  # Prevent index errors
    return example

dataset = dataset.map(add_metadata, with_indices=True)

# ========================
# Step 3: Save the dataset locally
# ========================
print(f"Saving dataset to {save_path}...")
dataset.save_to_disk(save_path)

# ========================
# Step 4: Upload to Hugging Face Hub (Optional)
# ========================
if push_to_hub:
    print("Logging in to Hugging Face Hub...")
    login(write_permission=True)  # You'll be prompted for your HF token

    print(f"Pushing dataset to {repo_name}...")
    dataset.push_to_hub(repo_name)

    print("Dataset successfully uploaded!")

print("✅ Done!")