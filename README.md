# YouTube video splitter - Automated pipeline

## Objective
The present pipeline downloads a given number of YouTube videos through it's API (exposed through pytube [1]) and splits each video into a $$k$$ user-defined [TODO] length segments.
A DB server (Docker container) is used as a metadata store in order to capture:
1. Video ID [str(11)]
2. Video extension (*e.g.* mp4, mov, etc.) [str]
3. Video length (in seconds) [int]
4. Clip location (download path) [str]
5. Insert time (determined through DB server) [datetime]

A CSV file is generated 

## Directory tree structure
```
├── data
│   ├── ingestion
│   │   ├── url_file
│   │   └── video_clips
│   │       └── 20230913
│   ├── metadata
│   │   └── database
│   │       ├── db_init.sql
│   │       └── dockerfile
│   └── process
│       └── 20230913
│           ├── report
│           │   └── report_20230913.csv
│           ├── UJETerHAdJE
│           └── X5Qa0oe81tE
├── init.sh
├── pipeline.sh
└── src
    ├── dependencies
    │   ├── add_record.py
    │   ├── downloader.py
    │   ├── __init__.py
    │   ├── metadata_schema.py
    │   ├── __pycache__
    │   └── splitter.py
    └── main.py
```

The pipeline consists of five layers:
1. **Ingestion layer** - Videos landing in this layer. Videos are saved under `video_clips` and separated by ingestion date `%Y%m%d`. Each video is saved using it's unique video ID; this is safer than saving the original name (which may contain non-ASCII characters)
2. **Process layer** - For each ingestion date, a report is generated (CSV file) which contains the previous metadata from each video. Moreover, each video is split in this layer and placed on a folder identified by the video ID
3. **Metadata layer** - The metadata layer contains metadata about each processed video (as discussed previously). It consists of a Postgres DB running on a Docker container.
4. **Orchestration layer** [TODO]
5. **Failure layer** [TODO]

## Setup Guide
- Install Docker (see installation [2])

```
sudo apt update; sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev \
libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git gcc make

curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

. ~/.bashrc

git clone "https://github.com/Vaporducky/video_to_pgdb"

cd video_to_pgdb

pyenv install -v 3.10.9
pyenv virtualenv 3.10.9 youtube_donwload
pyenv activate youtube_donwload
pip install -r requirements.txt
```

## Usage
Create a url_file under data/ingestion which contains YouTube video URLs which point to videos **under 6 minutes**; the pipeline will fail if this condition is not met.
Use

`bash pipeline.bash ./data/ingestion/url_file.txt`

to run the pipeline.

### Postgres DB
To connect to the DB you may use the following:
`docker exec -it pg_container psql postgres://username:secret@localhost:5432/metadata_store`

this will place you directly in the metadata_store DB.

### REFERENCES
[]
[2] https://docs.docker.com/desktop/install/linux-install/
