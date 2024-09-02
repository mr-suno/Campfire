import pyperclip

print("✨ More emoji support soon to come.")

try:
    Copy = input("\n⚙️ Copy to Clipboard (True if blank): ")
    Formula = "\\u{{{:X}}}".format(ord(input("👀 Enter an Emoji: ")))

    if not Copy or Copy in ["True", "T", "t", "true"]:
        pyperclip.copy(Formula)
        print("\n✅ Copied Emoji to Clipboard!")

    print(f"➡️ Result: {Formula}")

except Exception as error:
    print("❌ Something went wrong! Please try using a different emoji.")

input("\n👍 Press anything to continue ...")
