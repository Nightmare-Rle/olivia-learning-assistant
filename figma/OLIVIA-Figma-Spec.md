# O.L.I.V.I.A — Figma UI Specification

**App:** Online Learning Intelligent Interactive Assistant  
**Window:** 1200×800 (min 1000×700), Light mode, Green theme  
**Font:** Default customtkinter (Segoe UI / system) — exact families listed per component

---

## 1. Color Palette

| Token | Hex | Usage |
|---|---|---|
| `text-primary` | `#000000` | All body text, labels, headings |
| `text-accent` | `#1a73e8` | Markdown links, answer view tags |
| `frame-transparent` | `transparent` | Wrapper/layout frames |
| `frame-theme` | `ctk default` | Login frame background |
| `surface-cream` | `#FFF8F0` | Official portal boxes, subject cards, file cards |
| `surface-gold` | `#FFF0D0` | Markdown reader, doc editor canvas, slide selected |
| `surface-warm` | `#FFF5EB` | Status bars, slide nav, gen log |
| `surface-white` | `#ffffff` | Doc editor textbox, slide canvas |
| `surface-light` | `#f5f5f5` | Markdown code block |
| `card-k12` | `#A5D6A7` | K-12 Learning home card |
| `card-college` | `#90CAF9` | College Programs home card |
| `card-search` | `#FFCC80` | Web Search home card |
| `card-md` | `#CE93D8` | Markdown Reader home card |
| `card-create` | `#CE93D8` | Create Documents home card |
| `card-import` | `#80DEEA` | Imported Files home card |
| `card-answers` | `#F48FB1` | Answer Sheets home card |
| `card-gen` | `#FFAB91` | Generate Curriculum home card |
| `card-content` | `#CE93D8` | My Content home card |
| `card-admin` | `#B0BEC5` | Admin Panel home card |
| `btn-green` | `#81C784` / `#66BB6A` | Save, Play, LRMDS, Full Lesson |
| `btn-blue` | `#90CAF9` / `#42A5F5` | CHED, Generate Now |
| `btn-orange` | `#FFB74D` / `#FFA726` | New Document, Resize |
| `btn-deeporange` | `#FF8A65` / `#FF7043` | New Slide, Add Slide |
| `btn-red` | `#E57373` / `#EF5350` | Stop, Delete, Close tab |
| `btn-yellow` | `#FFD54F` / `#FFCA28` | Pause |
| `btn-bluegrey` | `#90A4AE` / `#78909C` | Close Tab (slide) |
| `btn-indigo` | `#7986CB` / `#64B5F6` | Bold/Italic/Underline (doc) |
| `btn-salmon` | `#FFAB91` / `#FF8A65` | Generate Lesson |
| `tb-doc` | `#FFB74D` | Document editor toolbar bg |
| `tb-slide` | `#FF8A65` | Slide editor toolbar bg |
| `tb-btn-hover-doc` | `#3B86E8` | Doc toolbar button hover |
| `tb-btn-hover-slide` | `#D95A3A` | Slide toolbar button hover |
| `tb-btn-fg` | `transparent` | Toolbar button default bg |
| `tb-btn-text` | `white` | Toolbar button icons/text |
| `diff-full-lesson` | `#81C784` | Full Lesson button |
| `diff-easy` | `#A5D6A7` | Easy button |
| `diff-medium` | `#FFE082` | Medium button |
| `diff-hard` | `#EF9A9A` | Hard button |
| `diff-practice` | `#CE93D8` | Practice button |
| `diff-full-assessment` | `#F48FB1` | Full Assessment button |
| `nav-prev-next` | `#FFE0B2` / `#E0C9A6` | Slide prev/next buttons |
| `border-thumb-selected` | `#FFAB91` | Selected slide thumbnail |
| `border-thumb` | `#ccc` | Unselected slide thumbnail |
| `tag-quote` | `#666666` | Markdown quote |
| `tag-hr` | `#cccccc` | Markdown horizontal rule |
| `tag-header` | `#333` | Answer view header |
| `tag-separator` | `#999` | All-answers separator |
| `tag-empty` | `#888` / `#888888` | Empty/unknown tags |
| `handle-blue` | `#1a73e8` | Image resize handle |
| `handle-white` | `white` | Image resize handle highlight |

---

## 2. Typography

| Usage | Size | Weight | Family |
|---|---|---|---|
| App title "O.L.I.V.I.A." | 32 | Bold | system |
| Login subtitle | 14 | Normal | system |
| "Created by" text | 10 | Normal | system |
| Login counts | 12 | Normal | system |
| Section title (Home, K-12, College) | 28 | Bold | system |
| Tab header | 20–24 | Bold | system |
| Card title | 20 | Bold | system |
| Card subtitle | 14 | Normal | system |
| "Click to open" | 12 | Normal | system |
| Form title | 18 | Bold | system |
| Form labels | 14 | Normal | system |
| Form entries | 12 | Normal | system |
| Form buttons | 14 | Bold | system |
| Status bar | 10 | Normal | system |
| Logout | 9 | Normal | system |
| K-12/College headings | 18 | Bold | system |
| Category/grade list buttons | 13 | Normal | system |
| Subject card title | 14 | Bold | system |
| Difficulty buttons | 10–11 | Normal | system |
| Back button | 11 | Normal | system |
| Search URL entry | 14 | Normal | system |
| Quick links | 13 | Bold | system |
| MD reader text | 13 | Normal | system |
| Imported file name | 13 | Normal | system |
| Imported file size | 10 | Normal | system |
| Filter buttons | 12 | Normal | system |
| Doc editor text | 12 | Normal | Arial (default) |
| Slide editor text | 18 | Normal | Arial |
| Toolbar buttons | 10–12 | Normal/Bold | system |
| Admin titles | 26 | Bold | system |
| Admin section titles | 16 | Bold | system |
| Admin form labels | 14 | Normal | system |
| Admin entries | 12 | Normal | system |
| Generate header | 16 | Bold | system |
| Generate log | 12 | Normal | system |
| Generate button | 15 | Bold | system |
| Answer sheet list | 11 | Normal | system |
| Answer key line count | 9 | Normal | system |
| Slide page label | 11 | Normal | system |

---

## 3. Screens / Frames

### 3.1 Login Screen
- **Frame**: Full-window centered column
- **Spacing**: `pady=(25,5)` top, `pady=15` bottom
- **Elements**:
  - `[O.L.I.V.I.A.]` — text label, size 32 bold, `#000000`
  - "Online Learning Intelligent Interactive Assistant" — size 14
  - "Created by NightmareRLE" — size 10
  - Login count string — size 12
  - "Select your role to sign in" — size 16 bold
  - 3 role buttons (Student / Teacher / Admin) — 180×50, size 16 bold, rounded
  - Or: first-run form (2×260w entries + Create Admin button)
  - Or: login form (2×260w entries + Sign In button)

### 3.2 Main Tab View
- **Container**: CTkTabview 1100×650
- **Tabs** (always): Home, K-12 Learning, College Programs, Web Search, Markdown Reader
- **Tabs** (teacher/admin): Answer Sheets, Imported Files, Create, Generate Curriculum, My Content
- **Tabs** (admin only): Admin Panel
- **Status bar**: 10px font, Shows: Internet status | Signed in as | K-12 count | College count | Language dropdown | Logout

### 3.3 Home Tab
- **Header**: "O.L.I.V.I.A." 28 bold + subtitle
- **Cards grid**: 2–3 column responsive grid
  - Card dimensions: ~280×160, rounded corners 15px
  - Card bg: colored per type (see palette)
  - Label: title 20 bold + subtitle 14 + "Click to open" 12
  - Cursor: hand2
- **Info bar**: Internet: Connected/Offline

### 3.4 K-12 Learning Tab / College Programs Tab
- **Header**: Title 28 bold | Language dropdown (English/Tagalog) | Official portal box
- **Portal box**: 200×90, `#FFF8F0`, rounded 12px, title + visit button
- **Content**: Two-panel layout (1:1 ratio)
  - **Left**: Scrollable grade/category list — buttons height 38, size 13
  - **Right**: Scrollable subject/program cards
    - Cards `#FFF8F0`, rounded 10px
    - Subject title 14 bold
    - Difficulty buttons: 75×28–30, colored per difficulty

### 3.5 Web Search Tab
- **URL bar**: Entry + "Open in Browser" button (140w)
- **Quick links**: YouTube, Google, DepEd, CHED, Wikipedia buttons (130×44, 13 bold)
- **Browser**: Embedded tkinterweb browser widget

### 3.6 Markdown Reader Tab
- **Toolbar**: "Open .md File" button | Language selector | Filename label
- **Content**: Full-height CTkTextbox `#FFF0D0`, size 13

### 3.7 Answer Sheets Tab
- **Search bar**: Search entry + Refresh button
- **"Show All Answers"** button
- **List**: Scrollable answer sheet list (left panel)
- **Viewer**: CTkTextbox `#FFF0D0`, size 13 + language selector
- **Title tag**: `#1a73e8`, difficulty colored

### 3.8 Imported Files Tab
- **Header**: Title + Import Folder button
- **Filter bar**: All | Images | PDFs | Videos | Text | Other (90×30)
- **File list**: Cards `#FFF8F0` with name + size + Open button
- **Viewer**: Tabbed view for text editor, image preview, video player, PDF

### 3.9 Create Tab
- **Sub-tabs**: Upload | Doc N | Slide N
- **Upload tab**: Import Folder + Upload File buttons + file list
- **Document editor toolbar** (bg `#FFB74D`):
  - Undo/Redo | Size 10–12 buttons
  - Font family (85w) + Font size (45w) option menus
  - Bold/Italic/Underline | Indigo buttons
  - Align L/C/R
  - Bullet / Numbered / Link
  - Insert Image / Open / Save / Save As / Close
- **Canvas**: White page with border, 12pt Arial textbox
- **Status bar**: `#FFF5EB` with filename, words, line

### 3.10 Slide Editor
- **Layout**: Left thumbnail panel (320h scroll) | Right slide view + toolbar
- **Thumbnails**: 120×80 white frames, 11px label, selected border `#FFAB91`
- **Toolbar** (bg `#FF8A65`): B/I/U, Font size, Text color, BG color, Insert image
- **Nav bar** (`#FFF5EB`): Prev/Next buttons (`#FFE0B2`) | Slide X of Y label
- **Canvas**: White 800×600, 18pt Arial

### 3.11 Generate Curriculum Tab
- **Sub-tabs**: Full Generate | Prompt Lesson
- **Full Generate**: Log textbox (`#FFF5EB`, disabled) + Generate Now button
- **Prompt Lesson**: Form with Level→Grade→Subject→Title→Content fields + Generate button

### 3.12 Admin Panel
- **Sub-tabs**: Manage Users | Backup & Restore | Change Password | Generate Curriculum
- **Manage Users**: Add user form + Student list + Teacher list
- **Backup & Restore**: Create Backup / Restore Backup buttons
- **Change Password**: Current/New/Confirm entries + Change button

### 3.13 My Content Tab
- **Header**: "My Created Lessons" 22 bold + Refresh button
- **List**: Scrollable file cards `#FFF8F0` + Open button

---

## 4. Spacing System

| Token | Value |
|---|---|
| `space-xs` | 2px |
| `space-sm` | 5px |
| `space-md` | 10px |
| `space-lg` | 15px |
| `space-xl` | 20px |
| `space-2xl` | 25px |
| `space-3xl` | 30px |
| `space-4xl` | 40px |

---

## 5. Border Radii

| Token | Value |
|---|---|
| `radius-sm` | 4px |
| `radius-md` | 10px |
| `radius-lg` | 12px |
| `radius-xl` | 15px |

---

## 6. Iconography (Emoji-based)

Category emojis for subject cards:

| Keyword | Emoji |
|---|---|
| mathematics, math, algebra, geometry, calculus, trigonometry, statistics, probability | 📐📊∫ |
| science, biology, chemistry, physics, earth | 🔬🧬🧪⚛️🌍 |
| english, reading, writing, literacy, language | 📖📚✍️🗣️ |
| filipino | 🇵🇭 |
| araling panlipunan, social studies | 🌏 |
| edukasyon sa pagpapakatao, values, ethics | 💚 |
| music, arts, pe, health | 🎵🎨🏃❤️ |
| technology, tle, computer, ict, robotics | 💻🔧🤖 |
| homeroom guidance | 🧭 |
| reference | 📌 |

---

## 7. Difficulty Color Coding

| Difficulty | Color | Hex |
|---|---|---|
| Full Lesson | Green | `#81C784` |
| Easy | Light Green | `#A5D6A7` |
| Medium | Yellow | `#FFE082` |
| Hard | Red | `#EF9A9A` |
| Practice | Purple | `#CE93D8` |
| Full Assessment | Pink | `#F48FB1` |
