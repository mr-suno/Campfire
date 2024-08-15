# Published 8/14/2024
# Author: Suno
# Repository: https://github.com/mr-suno/Hellfire

# TIP: Run this directly as a .py file, viewing it in a code editor
#      may mess the formatting up with the emojis.

import requests
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

def generateResults(Length: int) -> str:
   Characters = ascii_letters + digits + '_'
   return "".join(choice(Characters) for _ in range(Length))

def processUser(User: str, Index: int, Results_Queue: Queue) -> None:
   if checkUser(User):
      with Locked:
         Allowed.add(User)
      
      Results_Queue.put((Index, User))
        
def main():
   Threads = input("⚙️ How many threads (Can increase speed, \"5\" if unspecified): ")
   Length = input("📈 Username Length (\"10\" if no response, requires 5+): ")
   Generate_Amount = input("👁️ How many users (By default, set to return 25): ")

   print("")

   if not Length:
      Length = 10
   else:
      Length = int(Length)

      if Length <= 4:
         Length = 5

         print("❌ Automatically changed length to 5!\n")

   if not Threads:
      Threads = 5
   else:
      Threads = int(Threads)

   if not Generate_Amount:
      Generate_Amount = 25
   else:
      Generate_Amount = int(Generate_Amount)

   Unique = []
   while len(Unique) < Generate_Amount:
      New = generateResults(Length)
      if New not in Unique:
         Unique.append(New)

   Results_Queue = Queue()

   with ThreadPoolExecutor(max_workers=Threads) as Executor:
      futures = {
         Executor.submit(processUser, User, Index + 1, Results_Queue): User
         for Index, User in enumerate(Unique)
      }

      for Future in as_completed(futures):
         Future.result()

   Sorted_Results = sorted(Results_Queue.queue, key=lambda x: x[0])

   if len(Allowed) > 0:
      for Index, User in Sorted_Results:
         print(f"✅ Username → \"{User}\" ← is available. ——→ ({Index} of {Generate_Amount})")
   else:
      print("❌ No usernames found within scope.")

   print("\n←————————————————————————→")

   print(f"\n💫 {len(Allowed)} Available of {int(Generate_Amount)} Usernames.")

   input("\nPress \"Enter\" to continue ...")

if __name__ == "__main__":
   main()
