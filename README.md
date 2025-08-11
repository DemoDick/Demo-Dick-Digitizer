# Demo Dick Digitizer

Demo Dick Digitizer is a tool for creating torrent files from local organized stashapp files.

## Features

- Create `.torrent` files for any file or folder
- Customizable tracker URLs
- Simple and fast operation

## Usage

1. Run `database_maker.py` to set up the initial database.
2. Copy .env.example to .env and configure with your API_URL and API_TOKEN from stashapp
3. Run `import_organized.py` to import your organized stashapp files.
4. Run `torrent_maker.py` to create torrent files from your imported stashapp files.

## In Progress

- Exporting stash_id and info_hash pairs using `export_hashes.py`
- Improved error handling and logging
- Support for additional tracker configurations

## Requirements

- Python 3.x (if using the Python version)
- math
- sqlite3
- libtorrent
- dotenv

## License

This project is currently a work in progress (WIP) and does not yet have a finalized license. Please contact the author for more information regarding usage and distribution.

## Contributing

Pull requests and suggestions are welcome!
