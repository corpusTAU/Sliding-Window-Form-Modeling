
# conversions between integer/fifths notation [e.g. F=-1, A=3] to strings ["Bb", "C#"]

def pitch_to_int(pitch):
    if isinstance(pitch, int):
        return pitch # unchanged if int is received
    
    pitch = pitch.replace("-","b") # m21 names flats with - sign
    return "FCGDAEB".index(pitch[0])-1 + (len(pitch)-1)*7*((-1) if pitch[-1] == "b" else 1)

def int_to_pitch(x):
    return "FCGDAEB"[(x+1)%7] + ("b" if x<0 else "#") * abs(int(((x+1) - ((x+1)%7))/7))






