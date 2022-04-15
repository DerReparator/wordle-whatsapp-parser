# Wordle WhatsApp Parser

This is the Wordle WhatsApp Parser. It provides a way to gather data about played
wordle games from a WhatsApp chat backup file (currently _*.zip_).

## Usage

Simply execute the following line to try it out:

`python3 wordle-whatsapp.py --input="examples/WhatsApp Chat - example.zip"`

### Full instructions

1. Gather the chat backup *.zip file
    1. Open WhatsApp on your phone
    2. Navigate to the chat (likely a _Group_ chat) where you want to extract
    Wordle data from
    3. Click on the top of the chat window to open up the chat's "settings" view
    4. Scroll down and choose _Export Chat_
    5. Exclude media from the backup to reduce file size drastically
    6. Choose a location to save the *.zip file
2. Transfer the *.zip file to your PC / Mac where you run this python script
3. Execute the script on your Backup *.zip file with the command-line mentioned
above

## Stage of development

Currently, only the very basic parsing functionality is working. You will see
the data on your console when running this script.

Todo List:

- [ ] Include information about the sending person in the WhatsApp chat parser
- [ ] Better utilize the gathered data? Implement a graphical way to display data
- [ ] The german Wordle website [wordle.at](https://wordle.at/) uses a slightly
different format for its results which includes the current streak. Adapt the
parser to also handle this extended information.
- [ ] Support other data sources for Wordle results.

## For developers

You need at least **>= Python 3.8** to execute the code.

### What to do?

Check the above Todo List for missing features. Check the _Issues_ page for bugs
that were encountered and need fixing.

### Commit message format

Please respect the following rules for writing commit messages:

1. One change packet per line. Ideally, one commit only contains only on change
packet.
2. Use the following symbols to convey the specified meaning:
    1. `+` is used for describing _added_ features
    2. `*` is used for describing _changed_ features and _Bug fixes_
    3. `-` is used for describing _removed_ features
3. When using the above symbols, do **not** also describe the meaning by text.
F.e., use `+ filter function to foo` instead of `+ added filter function to foo`
.
