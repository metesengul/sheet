# Sheet
Sheet is a python script for processing midi files.

There are two classes: Message and Sheet
Sheet object holds a list of Message objects.
You can easily load midi files using "load_midis" function of a Sheet object, or turn Sheet objects into a midi file using "save_midi".

Basic implementation:
```
s = Sheet()
s.load_midis("./midi_files")
s.save_midi("./new_midi_file.midi")
```
Message objects have 4 properties: note, time, velocity, duration.
All of them are integers. 
Note property ranges from 0 to 87.
Velocity property ranges from 0 to 127
Time and Duration properties range from 0 to infinity.

You can create Sheet objects using a list of Message objects.

s = Sheet()

s.load_messages([Message(4,50,12,45), Message(10,100,5,5)])
