from __future__ import absolute_import

import time
import PySimpleGUI as sg
import os
import openai
from tkinter import * 
from tkinter import ttk
  


openai.api_key = "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"
openai.Model.list()
    


# SETTINGS:

element_pad = 5




# Example character to feed the AI, helps it know what to write in each box, however, it may just recycle the answers from the example
examplecharacter = ["Name:Greg", "Gender:Male", "Age:24", "Birthday:24th of september, 1988", "Hometown:Dublin", "Main Goal:Save The Day", "Desires:Be a hero", "Secrets:Doesn't believe in himself", "Quirks:Very outgoing", "Positive Traits:Friendly, agreeable", "Negative Traits:pushover,big temper", "Physical Traits:thin, athletic", "Ethnicity:white", "Hair Color:brown", "Eye Color:blue", "Height:5:11", "Body Type:skinny", "Fashion:fashion blind", "Piercings/Tattoos:dragon tattoo on left arm", "Birthmarks:birthmark on left forearm", "Known Languages:english", "Temperament:small fuse", "Learning Type:visual", "Religion:none", "Superstitions:flat earth", "Likes:campfires, horses", "Dislikes:goats, water", "Hobbies:gymnastics, flying RC planes","Immediate Family:father named Paul, mother named Linda", "Disant Relatives:none", "Friends:Daniel, Tim, Finn","Significant Other:none", "Archetypes:The innocent", "Tropes:the chosen one"]


# to stop the AI from recycling answers from the example, provide it with two.
examplecharacter2 = ["Name:Joe", "Gender:Male", "Age:65", "Birthday:1st of july, 2004", "Hometown:Bridgewater", "Main Goal:Get Rich", "Desires:Be rich", "Secrets:Lonely", "Quirks:Very quiet", "Positive Traits:Agreeable, joyful, funny", "Negative Traits:doesn't take anything seriously", "Physical Traits:overweight, slow", "Ethnicity:Black", "Hair Color:Black", "Eye Color:green", "Height:6:1", "Body Type:overweight", "Fashion:well dressed", "Piercings/Tattoos:none", "Birthmarks:birthmark on back", "Known Languages:elvish", "Temperament:patient", "Learning Type:listening", "Religion:christian", "Superstitions:none", "Likes:food, money", "Dislikes:spiders, birds", "Hobbies:investing, hiking","Immediate Family:father named Luis, mother named Miranda", "Disant Relatives:none", "Friends:none","Significant Other:Tina", "Archetypes:The annoying character", "Tropes:comedic relief"]

# general list of attributes, we'll loop through this when generating
attributes = ["Name", "Gender", "Age", "Date of birth", "Hometown", "Main Goal", "Desires", "Secrets", "Quirks", "Positive Traits", "Negative Traits", "Physical Traits", "Ethnicity", "Hair Color", "Eye Color", "Height", "Body Type", "Fashion", "Piercings/Tattoos", "Birthmarks", "Known Languages", "Temperament", "Learning Type", "Religion", "Superstitions", "Likes", "Dislikes", "Hobbies","Immediate Family", "Disant Relatives", "Friends","Significant Other", "Archetypes", "Tropes"]

# examples get saved to these strings
example=""
example2=""

for x in examplecharacter:
    example=example+x+"\n"
for x in examplecharacter2:
    example2=example2+x+"\n"

# the character gets saved to this string
character = ""




# Get a "windows" look
sg.LOOK_AND_FEEL_TABLE['Native'] = {
    'BACKGROUND': sg.COLOR_SYSTEM_DEFAULT,
    'TEXT':       sg.COLOR_SYSTEM_DEFAULT,
    'INPUT':      sg.COLOR_SYSTEM_DEFAULT,
    'TEXT_INPUT': sg.COLOR_SYSTEM_DEFAULT,
    'SCROLL':     sg.COLOR_SYSTEM_DEFAULT,
    'BUTTON':    (sg.COLOR_SYSTEM_DEFAULT, sg.COLOR_SYSTEM_DEFAULT),
    'PROGRESS':   sg.DEFAULT_PROGRESS_BAR_COLOR,
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}
# dunno what this does
# sg.wx.NO_BORDER = sg.wx.FRAME_SHAPED
# apply theme
sg.theme('Native')

# create layout ------

menu_def = [["File", ["Import", "Export", "Quit"]]]

element = []

for x in attributes:
    element.append([sg.Input(pad=(element_pad,element_pad), key="- " + x + " -"),sg.Button(x, pad=(element_pad,element_pad))])
element.append([sg.Button("Bio/Summary")])
element.append([sg.Push(), sg.Multiline("waiting to be generated...", key="- Bio/Summary -", size=(60, 15), pad=(5,5)), sg.Push()])

layout = [
[sg.Text(" - GPT-J Character Creator - ")],
[sg.Menu(menu_def, pad=(0,0))], 
[sg.Push(), sg.Column(element, size=(500,700), scrollable=True, pad=(0,0)), sg.Push()]

]


# layout end ------

# FUNCTIONS -----
def regenerateCharacter():
    charA = ""
    for x in attributes:
        val = values["- " + x + " -"]
        if len(val) != 0:

            charA = charA + x + ": " + val + "\n"
    # print("POOPFART :\n" + charA)
    return charA
    
def convert_to_float(string):
    # remove all non digits
    string = ''.join(c for c in string if c.isdigit() or c == '.')
    # convert to float
    return float(string)
            

def generateValue(element):
    keyA = "- " + element + " -"
    window[keyA].update("")
    values[keyA] = ""
    time.sleep(0.01)
    character = regenerateCharacter()
    
    
    prompt = example + "\n" + example2 + "\n" + character + element + ":"
    
    # model_inputs = { "text": prompt, "length": 8, "temperature": convert_to_float(values["-temp-"]), "topK": convert_to_float(values["-topK-"]), "topP": convert_to_float(values["-topP-"])}
                
    print("generating...")
    
    response = openai.Completion.create(
      model="text-curie-001",
      prompt=prompt,
      temperature=1.2,
      max_tokens=73,
      top_p=1,
      frequency_penalty=0.5,
      presence_penalty=0.25,
      stop=["\n"]
    )
    
    output = response['choices'][0]['text'].strip()
    
    print("output:\n")
    output = output.partition('\n')[0]
    
    print("Output: " + output)
    
    window[keyA].update(output)
    values[keyA] = output
    
    time.sleep(0.1)
    character = regenerateCharacter()
    time.sleep(0.01)
    
    #printCharacter()
    print("-------- char ----------")
    print(character);
    print("-------- char ----------")

def generateBio():
    character = regenerateCharacter()
    prompt = character + "Write a short but sweet summary/biography about the character:"
    # model_inputs = { "text": prompt, "length": 128, "temperature": 0.75, "topK": 50, "topP":1 }
            
    print("generating...")
    
    response = openai.Completion.create(
      model="text-babbage-001",
      prompt=prompt,
      temperature=0.7,
      max_tokens=128,
      top_p=1,
      frequency_penalty=0.7,
      presence_penalty=0.25,
    )
    
    output = response['choices'][0]['text'].strip()
    
    
    window["- Bio/Summary -"].update(output)
    values["- Bio/Summary -"] = output
    
    character = regenerateCharacter()

            
# helper function to quickly print the character
def printCharacter():
    print("----------- CHARACTER ---------------")
    print(character)
    print("-------------------------------------")
    
def save():
	Files = [('All Files', '*.*'),
			('Python Files', '*.py'),
			('Text Document', '*.txt')]
	file = asksaveasfile(filetypes = Files, defaultextension = Files)


# Create the window 
window = sg.Window("Demo", layout, font=("Helvetica",10), margins=(0,0))

# Create an event loop
while True:
    event, values = window.read()
    # program goes here
    if event == "Bio/Summary":
        generateBio()
    elif event == "Export":
        save()
    else:
        generateValue(event)
    
    
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

window.close()

        


       
