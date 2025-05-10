# MS_Search

A Nuke panel for quickly finding and zooming to nodes by name or type, with live filtering and a list.

![MS - Search](https://github.com/user-attachments/assets/1f3837e9-db36-42e6-abe9-b1c89f83a0c5)

---

## 🚀 Features

- **Live search** as you type 
- Shows node name, class, read filename and label  
- Centers the Node Graph on your chosen node  
- Compatible with Nuke 9+ (PySide, PySide2, PySide6)

---

## 📦 Requirements

- Nuke 9 or newer  
- Python 2.7 (for Nuke <11) or Python 3.x (for Nuke 11+)

---

## ⚙️ Installation

1. **Copy** `MS_Search.py` into your `~/.nuke` folder.  
2. **Edit** `~/.nuke/menu.py` and add:


nuke.menu("Node Graph").addCommand(
    "MS/Search Nodes…",
    "MS_Search.show_search_tool()",
    "," #replace ',' with any shortcut you like
)

3. **Restart Nuke**


## 💡 Usage
Press , (or your chosen shortcut) in the Node Graph to open the search panel.

Start typing to filter nodes by name or class.

Click any result to zoom directly onto that node.

## 🤝 Contributing
Found a bug or have a feature idea? Feel free to open an issue or send a pull request!

## Special thanks for 
Danilo de Lucio - Forever grateful for inspiring me to learn Python and always sharing knowledge.
https://danilodelucio.com/
