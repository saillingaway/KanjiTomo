## KanjiTomo 漢字トモ
KanjiTomo streamlines the otherwise awkward process of deciphering the unfamiliar Japanese in your Twitch chat. 
It eliminates the hassle of having to stop your streaming activities to look up a phrase, reading or kanji.

### How it works
KanjiTomo connects to your Twitch account and forwards the chat messages straight to [Jisho.org](https://jisho.org), one of the most useful Japanese translation tools available online. 
The message's particles and endings are stripped using [Cabocha](), a Japanese N.L.P./Structure Analyzer, to leave only the core phrases and characters. 
Then the phrases are opened in the browser on Jisho.org for you to see and interpret based on context.

### Set up
**KanjiTomo is meant for streams with lower traffic. I don't recommend this for streams with consistently busy chats. I'm working on an update to handle heavier streams**

To set up KanjiTomo, after you download the files on your machine create a new file `tomo.ini`. 
Copy the contents of [`examples/config-tomo.ini`](examples/config-tomo.ini) into the new file, and replace with your Twitch credentials (to get a Twitch Chat Oauth Password, go [here](https://twitchapps.com/tmi/)).

Alternatively, you can fill in your credentials in `config-tomo.ini` and rename the file to `tomo.ini`.

When you start your stream simply run `tomo.py` like any other python file. 
Tomo will open each Jisho.org message in a new tab.

### Features in Progress
- Language detection
- Frontend functionality (to eliminate numerous tabs in a browser)
   - options to save or export characters, phrases and entries
- Coloring characters based on frequency or JLPT level

### Idea
Talking to native speakers was the best way that I improved my language skills. I got the idea for this after starting a streaming channel where I reviewed JLPT Kanji, read books, and talked about all kinds of things with native speakers through the chat.
