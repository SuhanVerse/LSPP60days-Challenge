# Day 31: Python Basics Demo


hastags: list = ["#Python", "#NEXT30", "#AI"]
greet: str = "Hello, Leapfrog"
year:int = 2025
pi: float = 3.14
stat: bool  = True

print(greet)
print(" ".join(hastags))
print(f"Current Year: {year}")
print("Value of π :", pi)
print("Is the challenge active?", stat)
print()  # prints a new line


a = 43
b = 3

print(f"{a} + {b} =", a + b)
print(f"{a} - {b} =", a - b)
print(f"{a} * {b} =", a * b)
print(f"{a} / {b} =", a / b)    # this will give a normal division result 
print(f"{a} // {b} =", a // b)  # this gives a rounded off division result 
print(f"{a} % {b} =", a % b)    
print(f"{a} ** 2 =", a ** 2)    
print()  

def summarize():
    """Prints a summary of data types that has been used"""
    types = {
        'hashtags': type(hastags).__name__,
        'greet': type(greet).__name__,
        'year': type(year).__name__,
        'pi': type(pi).__name__,
        'stat': type(stat).__name__
    }
    print("\nVariable Types Summary:")
    for var, t in types.items():
        print(f" - {var}: {t}")

summarize()

print()
songs = ["Kale Dai Kale Dai", "Sapphire", "DAN DAN"]
print("Original list:", songs)
print("First song:", songs[0])
print("Last song:", songs[-1])
print("Slice songs[1:3]:", songs[1:3])
songs.append("Line without a hook")
print("After append():", songs)
print("Total songs count:", len(songs))
print()

song = {
    "title": "Sapphire",
    "artist": "ED Sheeran",
    "year": 2025,
    "genre": "Pop",
}
print("Song dict:", song)
print("Title field:", song["title"])
song["duration"] = 184
print("After adding duration:", song)
print("Iterating key–value pairs:")
for key, val in song.items():
    print(f"  {key}: {val}")
print()

def servo_angle(rpm):
    if rpm < 90:
        return "Acute"
    elif rpm > 180:
        return "Obtuse"
    else:
        return "Angle: "f"{rpm}"

for rpm in [45, 230, 140]:
    print(f"{rpm} RPM is {servo_angle(rpm)}")
print()

def playlist(psong):
    """Print each song title with numbering."""
    for i, title in enumerate(psong, start=1):
        print(f"{i}. {title}")

my_songs = ["Uptown Funk", "Sapphire", "End of Beginning", "Line without a hook"]
print("My Playlist:")
playlist(my_songs)
print()