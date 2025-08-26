import kagglehub

# Download latest version
path = kagglehub.dataset_download("shubhammehta21/movie-lens-small-latest-dataset")

print("Path to dataset files:", path)