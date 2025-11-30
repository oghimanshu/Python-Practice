# Data Analysis with Python - Interactive Teaching Platform

## 🚀 Quick Start (60 Seconds)

1. **Open in Browser:**
   - Simply open `index.html` in any web browser
   - No installation, no build tools, no setup required
   - Everything works immediately with internet connection

2. **That's it!** 
   - All content, styles, and interactive features load from CDNs
   - Fully functional teaching platform ready to use

---

## 📋 Requirements

**Minimum:**
- ✅ Internet connection
- ✅ Modern web browser (Chrome, Firefox, Safari, Edge)

**Optional (for live Grammy data):**
- Python 3.8+
- Dependencies in `requirements_new.txt`

---

## 🎨 Features

### Core Features
- **10+ Interactive Topics** with detailed explanations
- **Chart.js Visualizations** for data analysis concepts
- **Grammy Awards Capstone** project with real Kaggle data
- **AMOLED Dark Mode** with auto-persistence
- **Responsive Design** (mobile, tablet, desktop)
- **FAQ, Glossary, References** sections

### Technical Features
- Pure HTML/CSS/JavaScript (no build tools)
- CSS Variables for unified theming
- Smooth 0.4s transitions for dark mode
- Chart theme auto-updates with dark mode toggle
- localStorage persistence for theme preference
- Error-tolerant: gracefully handles missing resources

---

## 🌓 Dark Mode

**How it works:**
1. Click the **sun/moon icon** in the header (top-right)
2. Theme preference saves automatically
3. Reloads with same theme on next visit
4. Pure AMOLED black (#000000) for OLED displays

**What changes:**
- Background: Light gray → Pure black
- Text: Dark gray → Light gray
- Borders: Light → Dark
- Charts: Auto-update colors and grid

---

## 🎵 Grammy Analytics (Optional Server)

### Without Server (Uses Fallback Data)
- Charts display with sample data automatically
- No errors or missing features
- Works perfectly offline after first load

### With Server (Live Data)
1. **Install dependencies:**
   ```bash
   pip install -r requirements_new.txt
   ```

2. **Start the server:**
   ```bash
   python grammy_server.py
   ```

3. **Browser will auto-detect:**
   - Fetches live data from http://localhost:5000/api/grammy
   - Updates charts within 2 seconds
   - Shows "Charts updated from server payload" message

4. **Dataset source:**
   - Kaggle: johnpendenque/grammy-winners-and-nominees-from-1965-to-2024
   - Fetched via MLCroissant (Croissant JSON-LD format)
   - No disk writes, all in-memory streaming

---

## 📁 File Structure

```
index.html                    # Main teaching platform (all-in-one)
requirements_new.txt          # Optional: Python dependencies
grammy_server.py              # Optional: Flask backend for live data
requirements_new.txt          # Optional: Updated Python packages
```

---

## 🔍 What's Inside

### Topics (1-10)
1. **Data Ingestion** - CSV, JSON, APIs
2. **NumPy Operations** - Vectorization, arithmetic
3. **Advanced Slicing** - Boolean indexing, fancy indexing
4. **Array Metadata** - Memory, dtypes, reshape
5. **DataFrames** - Pandas fundamentals
6. **Basic GroupBy** - Aggregation basics
7. **Multi-Aggregation** - Complex grouping
8. **Merging Data** - Joins and concatenation
9. **Data Integrity** - Cleaning, handling missing values
10. **Trade Case Study** - Real-world application

### Capstones
- **Kendrick Lamar** - Narrative analysis with automated slideshow
- **Grammy Awards** - Multi-dimensional data visualization

### Resources
- **FAQ** - Common questions with detailed answers
- **Glossary** - 10+ data analysis terms
- **References** - APA 7 formatted academic citations

---

## 🎯 Dark Mode Technical Details

### CSS Variables (Updated on Toggle)
```css
:root {
  --text-primary: #1e293b;      /* Light: dark gray */
  --text-heading: #0f172a;      /* Light: very dark */
  --bg-body: #f8fafc;           /* Light: off-white */
  --bg-panel: #ffffff;          /* Light: white */
}

.dark {
  --text-primary: #e2e8f0;      /* Dark: light gray */
  --text-heading: #f8fafc;      /* Dark: near white */
  --bg-body: #000000;           /* Dark: pure black */
  --bg-panel: #0a0a0a;          /* Dark: very dark */
}
```

### How It Works
1. JavaScript toggles `.dark` class on `<html>` and `<body>`
2. CSS variables automatically switch values
3. All colors inherit from variables (no hardcoded colors)
4. Chart.js colors update in real-time
5. 0.4s ease transitions make changes smooth

---

## 🌐 Browser Compatibility

| Browser | Desktop | Mobile | Status |
|---------|---------|--------|--------|
| Chrome | ✅ Latest | ✅ Latest | Fully supported |
| Firefox | ✅ Latest | ✅ Latest | Fully supported |
| Safari | ✅ Latest | ✅ Latest | Fully supported |
| Edge | ✅ Latest | N/A | Fully supported |
| Mobile Safari | N/A | ✅ Latest | Fully supported |
| Chrome Mobile | N/A | ✅ Latest | Fully supported |

---

## 📊 Technologies Used

**Frontend:**
- Tailwind CSS v3 (CDN)
- Chart.js 4 (CDN)
- PapaParse 5 (CSV parsing, CDN)
- Google Fonts: Inter (CDN)
- Unsplash Images (CDN)

**Backend (Optional):**
- Flask 2.0+
- Pandas 1.3+
- MLCroissant 0.2+
- CORS enabled for cross-origin requests

**All external resources have fallbacks - if CDN fails, fallback data is used**

---

## 🚀 Deployment Options

### Option 1: Simple (Recommended)
```bash
# Just open in browser
open index.html          # macOS
start index.html         # Windows
xdg-open index.html      # Linux
```

### Option 2: Local Server
```bash
# Python simple HTTP server
python -m http.server 8000
# Visit: http://localhost:8000
```

### Option 3: With Flask Backend
```bash
# Start Grammy data server
python grammy_server.py
# Open http://localhost:5000 in browser
# Or open index.html, it will auto-detect
```

### Option 4: Production Deploy
- Upload `index.html` to any web host (Netlify, GitHub Pages, etc.)
- Works instantly, no build step needed
- Optional: Deploy `grammy_server.py` to separate server with CORS enabled

---

## 🔒 Privacy & Security

- **No tracking:** No analytics, no cookies, no user data collection
- **Local storage only:** Theme preference stored in browser only
- **No server required:** Core functionality works completely offline (after first load)
- **Optional API:** Grammy data API is opt-in and gracefully fails if unavailable

---

## 📝 Customization

### Change Styling
Edit CSS variables in `<style>` section:
```css
:root {
  --text-primary: #1e293b;    /* Change text color */
  --bg-body: #f8fafc;         /* Change background */
  --accent-color: #2563eb;    /* Change accent */
}
```

### Add New Topics
1. Create new `<div id="topic11" class="topic-panel hidden">` section
2. Add link in sidebar nav
3. Add `switchTopic()` event handler
4. Charts auto-initialized with defensive checks

### Change Dark Mode Colors
Edit `.dark` CSS variables:
```css
.dark {
  --bg-body: #000000;         /* AMOLED pure black */
  --text-primary: #e2e8f0;    /* Light gray text */
}
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Charts not showing | Ensure JavaScript is enabled, wait for CDN load |
| Dark mode not working | Clear browser cache, check localStorage is enabled |
| Grammy data not loading | Server optional - sample data displays automatically |
| Fonts look wrong | Check internet connection (Google Fonts CDN) |
| Images not loading | Check internet connection (Unsplash CDN) |

---

## 📞 Support

For issues or questions:
1. Check browser console (F12 → Console tab)
2. Verify internet connection
3. Try different browser
4. Clear cache and reload

---

## 📄 License & Attribution

- **Content:** Faculty: Himanshu Gaur
- **Design:** Modern responsive teaching platform
- **Dependencies:** 
  - Tailwind CSS (MIT)
  - Chart.js (MIT)
  - PapaParse (MIT)
  - Kaggle Dataset (Dataset specific license)

---

## ✨ Latest Updates

✅ **Dark Mode Fixed**
- All text now properly visible in both themes
- Toggle buttons always accessible
- Smooth 0.4s transitions

✅ **Universal Compatibility**
- Works with just internet + browser
- No installation required
- Graceful fallbacks for all features

✅ **Grammy Analytics**
- Live Kaggle data via MLCroissant
- Optional Flask server
- Auto-fallback to sample data

✅ **CSS Variable Theming**
- All colors from CSS variables
- No hardcoded colors blocking visibility
- Charts auto-update on theme change

---

**Ready to start learning Data Analysis with Python?** Open `index.html` now! 🎓
