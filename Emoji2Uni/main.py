import pyperclip

Copy = input("⚙️ Copy to Clipboard (True if blank): ")
Formula = "\\u{{{:X}}}".format(ord(input("👀 Enter an Emoji: ")))

if not Copy or Copy in ["True", "T", "t", "true"]:
    pyperclip.copy(Formula)
    print("\n✅ Copied Emoji to Clipboard!")

print(f"\n➡️ Result: {Formula}")
