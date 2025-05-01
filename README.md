# League of Legends Patch Skin Image Scraper

This tool downloads high-quality skin images from official League of Legends patch note pages.

It scans multiple patch versions, locates skin sections based on their visual containers, and names the images using their associated skin titles.

---

## 🔧 Features

- Scrapes patch note pages starting from Patch 11.1
- Finds skin images by locating a nearby paragraph:  
  `"The following skins will be released in this patch"`
- Supports `<p>` with or without the `summary` class
- Detects `div.skin-box` blocks inside the correct section
- Downloads images from `cmsassets.rgpub.io` directly
- Names files using the official skin name from `skin-title`
- Skips image resolution filtering (downloads all found skins)
- Avoids duplicates and re-downloading

---

## 📦 Requirements

- Python 3.7+
- pip (Python package manager)

### Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## 🚀 Usage

```bash
python scraper.py
```

By default, it starts from patch 11.1 and checks all valid patch URLs incrementally (e.g., `patch-11-1`, `patch-11-2`, ..., `patch-14-10`).

All downloaded skins will be saved in the `skins/` folder using readable file names like:

```
skins/Lunar Beast Viego.jpg
skins/Prestige Spirit Blossom Lux.jpg
```

---

## 🗂 Folder Structure

```
.
├── scraper.py
├── skins/
│   ├── Skin 1.jpg
│   ├── Skin 2.jpg
│   └── ...
└── README.md
```

---

## 🔍 How It Works

1. The script builds patch URLs and fetches HTML pages.
2. It searches for a `<p>` element containing "The following skins will be released".
3. From the closest parent `div`, it finds all `.skin-box` elements.
4. For each `.skin-box`, it extracts the image URL and the skin name.
5. Images are downloaded using the direct link and saved with clean names.

---

## 📌 Notes

- Only works with publicly available patch notes on [leagueoflegends.com](https://www.leagueoflegends.com/)
- Only images hosted on `cmsassets.rgpub.io` are downloaded.
- Doesn’t rely on JavaScript. Works purely via HTML parsing.
- If a patch does not contain skins, it skips gracefully.

---

## 🛡 License

MIT License – do whatever you want with it, but don’t blame me.

---

## 🙋‍♂️ Author

Created by [Manula Sameera](https://github.com/manula-sameera) – Feel free to open issues or suggest improvements.
