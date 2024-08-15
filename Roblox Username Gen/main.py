# Published 8/14/2024
# Author: Suno
# Repository: https://github.com/mr-suno/Hellfire

# TIP: Run this directly as a .py file, viewing it in a code editor
#      may mess the formatting up with the emojis.

# P.S. I love you! -Sincerely, Suno

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

def generateResults(Length: int) -> str:
   Characters = ascii_letters + digits + '_'
   return "".join(choice(Characters) for _ in range(Length))

def processUser(User: str, Index: int, Results_Queue: Queue) -> None:
   if checkUser(User):
      with Locked:
         Allowed.add(User)
      
      Results_Queue.put((Index, User))

def estimateCheck(Sample: int = 10) -> float:
   Start = time.time()
   for _ in range(Sample):
      checkUser("test_user")
   Stop = time.time()
   return (Stop - Start) / Sample
        
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
      if int(Threads) < 1:
         Threads = 5
         print("⚠️ Automatically assigned 5 threads due to invalid thread count!")
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

   Estimated_Time = estimateCheck()

   Total_Checks = len(Unique)
   Total_Estimated_Time = Total_Checks * Estimated_Time
   Thread_Time = Total_Estimated_Time / Threads
   
   if Threads > 30:
      Thread_Time = (Total_Estimated_Time / Threads) + 5

   if int(Threads) > 1:
      print(f"⚙️ Attempting to Process: {Generate_Amount} usernames with {Threads} threads.")
   else:
      print(f"⚙️ Attempting to Process: {Generate_Amount} usernames with {Threads} thread.")

   print(f"⚠️ Estimated Wait Time: {Thread_Time:.2f} seconds ... (Possibly a Bit Off)")

   print("")

   Start = time.time()

   with ThreadPoolExecutor(max_workers=Threads) as Executor:
      futures = {
         Executor.submit(processUser, User, Index + 1, Results_Queue): User
         for Index, User in enumerate(Unique)
      }

      for Future in as_completed(futures):
         Future.result()

   Elapsed = time.time()
   Total_Time = Elapsed - Start

   Sorted_Results = sorted(Results_Queue.queue, key=lambda x: x[0])

   if len(Allowed) > 0:
      for Index, User in Sorted_Results:
         print(f"✅ Username → \"{User}\" ← is available. ——→ ({Index} of {Generate_Amount})")
   else:
      print("❌ No usernames found within scope.")

   print("\n←————————————————————————→")

   print(f"\n💫 {len(Allowed)} Available of {int(Generate_Amount)} Usernames.")
   print(f"⏱️ Total Time Taken: {Total_Time:.2f} seconds.")

   input("\nPress \"Enter\" to continue ...")

if __name__ == "__main__":
   main()
