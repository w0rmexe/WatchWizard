# WatchWizard

A Windows 95-styled application that helps you decide what to watch by randomly selecting from your curated list of movies, TV shows, and kids' content.

## Features

- Random selection from different categories (Movies, TV Shows, Kids)
- Windows 95 aesthetic with classic UI elements
- Easy management of your watchlist
- Keyboard shortcuts for quick access
- Add and remove items from your watchlist
- View all items in each category

## Installation

1. Clone this repository or download the source code
2. Make sure you have Python 3.x installed
3. Run the program:
   ```bash
   python WatchWizard.py
   ```

## Usage

### Main Window
- Click buttons or use keyboard shortcuts to select content:
  - `M`: Pick a Movie
  - `T`: Pick a TV Show
  - `K`: Pick Kids Content
  - `R`: Pick Random from All
  - `V`: View List

### View List Window
- View all items in a category
- Add new items
- Remove selected items
- Navigate between categories

### Adding Items
- Click "Add New Item" or use the View List window
- Select the category (Movie, TV Show, or Kids)
- Enter the title
- Click Save

### Removing Items
- Open the View List window
- Select the category
- Select the item to remove
- Click "Remove Selected"

## File Structure

- `WatchWizard.py`: Main application file
- `watchlist.txt`: Stores your list of movies, TV shows, and kids' content

## Requirements

- Python 3.x
- tkinter (usually comes with Python)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 