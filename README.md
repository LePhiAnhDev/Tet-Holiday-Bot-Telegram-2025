# TET HOLIDAY BOT TELEGRAM 2025

### 1. Obtain **Telegram Bot Token**
1. Open Telegram and search for **@BotFather**.
2. Type the command `/newbot` to create a new bot.
3. Follow the instructions, provide a name and username for your bot.
4. Once created, you will receive a **Token**. Save this token and add it to the line `TOKEN = 'ENTER YOUR BOT TOKEN'` in the source file.

---

### 2. Install Required Libraries
Run the following command to install the necessary third-party libraries:
`pip install nest_asyncio pyinstaller python-telegram-bot`

---

### 3. Add **Telegram Token**
Copy the token you obtained from **@BotFather** and enter it in the line:
TOKEN = 'ENTER YOUR BOT TOKEN'

---

### 4. Running the Project
1. Open a terminal in the directory containing the source file.
2. First, check in the IDE. If everything is set up correctly, the bot will start listening for commands on Telegram. Then, it's time to package the bot.
3. You can also run the command to start the bot in the terminal (note that the terminal running the command must be in the same folder as the TetHolidayBot.py file):
`python TetHolidayBot.py`

---

### 5. Packaging the Project with PyInstaller
1. Package the source file into a standalone `.exe` file:
`pyinstaller --onefile TetHolidayBot.py`
2. The executable file will be saved in the `dist/TetHolidayBot.exe` directory.

---

## Author
**Lê Phi Anh**  

## Contact for Work
- Discord: LePhiAnhDev  
- Telegram: @lephianh386ht  
- GitHub: [LePhiAnhDev](https://github.com/LePhiAnhDev)
