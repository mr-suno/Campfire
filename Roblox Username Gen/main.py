# Published 8/14/2024
# Author: Suno
# Repository: https://github.com/mr-suno/Hellfire

# TIP: Run this directly as a .py file, viewing it in a code editor
#      may mess the formatting up with the emojis.

import requests
import time
from random import choice
from string import ascii_letters, digits
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from queue import Queue

Allowed = set()
Locked = Lock()

def checkUser(User: str) -> bool:
   URL = f"https://auth.roproxy.com/v1/usernames/validate?request.username={User}&request.birthday=2000-01-01"

   try:
      Response = requests.get(URL)

      if Response.status_code == 200:
         Status = Response.json().get("code")
         
         return Status == 0
   except requests.RequestException:
      pass

   return False

def generateResults(Length: int, Digits_Only: bool) -> str:
   global Characters
   if not Digits_Only:
      Characters = ascii_letters + digits + "_"
   else:
      Characters = digits
   return "".join(choice(Characters) for _ in range(Length))

def processUser(User: str, Index: int, Results_Queue: Queue, Generate_Amount: int) -> None:
   if checkUser(User):
      with Locked:
         Allowed.add(User)
      
      Results_Queue.put((Index, User))
      print(f"✅ Username → \"{User}\" ← is available. ——→ ({Index} of {Generate_Amount})")

def estimateCheck(Sample: int = 10) -> float:
   Start = time.time()
   for _ in range(Sample):
      checkUser("test_user")
   Stop = time.time()
   return (Stop - Start) / Sample
        
def main():
   Threads = input("⚙️ How many threads (Can increase speed, \"150\" if unspecified): ")
   Length = input("📈 Username Length (\"10\" if no response, requires 5+): ")
   Numbers_Only = input("💎 Enable Numbers-Only Usernames (\"false\" if left blank): ")
   Generate_Amount = input("👁️ How many users (By default, set to return 25): ")

   print("")

   if int(Threads) > 1:
      print(f"⚙️ Attempting to Process: {Generate_Amount} usernames with {Threads} threads.")
   else:
      print(f"⚙️ Attempting to Process: {Generate_Amount} usernames with {Threads} thread.")

   if not Length:
      Length = 10
   else:
      Length = int(Length)

      if Length <= 4:
         Length = 5

         print("❌ Automatically changed length to 5!\n")

   if not Threads:
      Threads = 150
   else:
      if int(Threads) < 1:
         Threads = 150
         print("⚠️ Automatically assigned 150 threads due to invalid thread count!")
      else:
         Threads = int(Threads)

   Only_Digits = False
   if Numbers_Only in ["True", "T", "true", "t"]:
      Only_Digits = True
   elif Numbers_Only in ["False", "F", "false", "f"]:
      Only_Digits = False
   else:
      Only_Digits = False

   if not Generate_Amount:
      Generate_Amount = 25
   else:
      Generate_Amount = int(Generate_Amount)

   Unique = []
   while len(Unique) < Generate_Amount:
      New = generateResults(Length, Digits_Only=Only_Digits)
      if New not in Unique:
         Unique.append(New)

   Results_Queue = Queue()

   print("")

   Start = time.time()

   with ThreadPoolExecutor(max_workers=Threads) as Executor:
      futures = {
         Executor.submit(processUser, User, Index + 1, Results_Queue, Generate_Amount): User
         for Index, User in enumerate(Unique)
      }

      for Future in as_completed(futures):
         Future.result()

   Elapsed = time.time()
   Total_Time = Elapsed - Start

   Sorted_Results = sorted(Results_Queue.queue, key=lambda x: x[0])

   if len(Allowed) > 0:
      print("")

   print("←————————————————————————→")

   print("")

   if len(Allowed) > 0:
      print(f"\n💫 {len(Allowed)} Available of {int(Generate_Amount)} Usernames.")
   else:
      print("❌ No usernames found within scope.")

   print(f"⏱️ Total Time Taken: {Total_Time:.2f} seconds.")

   input("\nPress \"Enter\" to continue ...")

if __name__ == "__main__":
   main()
