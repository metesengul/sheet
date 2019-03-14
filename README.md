# Sheet
Sheet is a python script for processing midi files.

Sheet uses NumPy and Mido, so don't forget to "pip install" them before using it.

There are two classes: Message and Sheet
Sheet object holds a list of Message objects.
You can easily load midi files using "load_midis" function of a Sheet object, or turn Sheet objects into a midi file using "save_midi".

Basic implementation:
```python
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
```python
s = Sheet()
s.load_messages([Message(4,50,12,45), Message(10,100,5,5)])
s.save_midi("./new_midi_file.midi")
```

You can turn Sheet objects into NumPy arrays.
```python
s = Sheet()
s.load_messages([Message(4,50,12,45), Message(10,100,5,5)])
n = s.to_array()
```

Check out the source file for more information about function parameters and such.
