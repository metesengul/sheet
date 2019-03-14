import mido
import glob
import numpy as np


class Message:
    def __init__(self, note, time, velocity, duration):
        self.note = note
        self.time = time
        self.velocity = velocity
        self.duration = duration

    def __str__(self):
        return "Message(Note: " + str(self.note) + \
               ", Time: " + str(self.time) + \
               ", Velocity: " + str(self.velocity) + \
               ", Duration: " + str(self.duration) + ")"


class Sheet:

    def __init__(self):
        self.messages = []
        self.midi_beginnings = []

    def load_midis(self, folder, resolution=100):
        messages = []
        for file in glob.glob(folder + "/*.mid*"):
            print("Loading " + file)

            for msg in mido.MidiFile(file):
                messages.append(msg)

        print("All files loaded.")

        midi_starts = [0]

        new_messages = []
        for i, msg in enumerate(messages):

            if msg.type == "end_of_track":
                midi_starts.append(len(new_messages) - midi_starts[-1])

            if msg.type[0:4] == "note" and msg.velocity != 0:

                # Find time
                j = i - 1
                t = msg.time
                while True:
                    if messages[j].type[0:4] == "note" and messages[j].velocity != 0:
                        break
                    t += messages[j].time
                    j -= 1
                time = t

                # Find duration
                j = i + 1
                n = msg.note
                d = 0
                while True:
                    d += messages[j].time
                    if messages[j].type[0:4] == "note" and \
                            messages[j].note == n and \
                            messages[j].velocity == 0:
                        break
                    j += 1
                duration = d

                note = int(msg.note)
                time = int(time * resolution)
                velocity = int(msg.velocity)
                duration = int(duration * resolution)
                if duration == 0:
                    duration = 1

                new_messages.append(Message(note, time, velocity, duration))
        self.messages = new_messages
        self.midi_beginnings = midi_starts[:-1]

    def load_messages(self, messages):
        self.messages = messages

    def save_midi(self, path, scale=9.7):
        s = list(np.transpose(self.to_array()))

        for i in s:
            i[1] = int(i[1] * scale)
            d = int(i[3] * scale)
            if d == 0:
                d = 1
            i[3] = d

        for i in range(len(s)):
            if i != 0:
                s[i][1] += s[i - 1][1]

        messages = []
        for i in range(len(s)):
            s.append([s[i][0], s[i][1] + s[i][3], 0, s[i][3]])

        s = sorted(s, key=lambda x: x[1])
        for i in reversed(range(len(s))):
            if i != 0:
                s[i][1] = s[i][1] - s[i - 1][1]

        for i in s:
            messages.append([i[0], i[1], i[2]])

        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)

        for msg in messages:
            track.append(mido.Message(type="note_on", note=int(msg[0]), time=int(msg[1]), velocity=int(msg[2])))

        mid.save(path)
        print("Saved to " + path)

    def to_array(self):
        array = np.zeros((4, len(self)))
        for i in range(len(self.messages)):
            array[0, i] = self[i].note
            array[1, i] = self[i].time
            array[2, i] = self[i].velocity
            array[3, i] = self[i].duration
        return array

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, item):
        return self.messages[item]
