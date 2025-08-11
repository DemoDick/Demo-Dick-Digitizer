# Demo Dick Digitizer

Demo Dick Digitizer is a tool for creating torrent files from local organized stashapp files.

## Features

- Create `.torrent` files for any file or folder
- Customizable tracker URLs
- Simple and fast operation

## Usage

1. Set up your database with `database_maker.py`.
2. Configure your API credentials in the `.env` file.
3. Import your organized stashapp files with `import_organized.py`.
4. Add tracker urls into the "tracker-list" table inside the torrent_maker.db
5. Generate torrent files with `torrent_maker.py`.

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
