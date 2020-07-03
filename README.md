# Google-Image-Downloader
Downloads bulk images from google. Useful for creating dataests
- downloads original images
- multithreaded for better performance
## Requirements
- selenium
- os
- requests
- threading
- time
- argparse
## Usage
```
downloader.py [-h] [-k search_term] [-N num__of_images] [-t num_of_threads]
```
- only the search term is a mandatory field

### Example
- downloads first 10 images from the results of google image search of "dog". Uses max 15 threads
```
downloader.py -k "dog" -N 10 -t 15
```
- downloads first 50 images from the results of google image search of "bear". Uses max 10 threads
```
downloader.py -k "bear"
```
