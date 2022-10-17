from __future__ import absolute_import

import time
# mport PySimpleGUI as sg
import PySimpleGUI as sg
import os
import openai
import tkinter as tk
from tkinter import * 
from tkinter import ttk
from tkinter import filedialog

openai.api_key = "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"
openai.Model.list()
    
# SETTINGS:
element_pad = 1

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
    'SLIDER_DEPTH': 1,
    'PROGRESS_DEPTH': 1,
}
# dunno what this does
# sg.wx.NO_BORDER = sg.wx.FRAME_SHAPED
# apply theme
sg.theme('Native')

# create layout ------

menu_def = [["File", ["Import", "Export", "Quit"]]]

element = []

for x in attributes:
    element.append([sg.Button(x, pad=(element_pad,element_pad)),sg.Push(),sg.Input(pad=(element_pad,element_pad), key="- " + x + " -")])
element.append([sg.Push(),sg.Button("Bio/Summary"), sg.Push()])
element.append([sg.Multiline("generate your bio!", key="- Bio/Summary -", size=(65, 10), pad=(0,0))])
element.append([sg.Push(),sg.Input("put your question here", key="question"), sg.Button("Ask"), sg.Push()])
element.append([sg.Multiline("ask a question!", key="answer", size=(65, 5), pad=(0,0))])

layout = [
[sg.Push(),sg.Text(" - GPT-J Character Creator - "),sg.Push()],
[sg.Text("Open API Key:"), sg.Input("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", password_char='*', key="key")],
[sg.Menu(menu_def, pad=(0,0))], 
[sg.Column(element, scrollable=True, vertical_scroll_only=True, size=(500,700), pad=(0,0))]
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
    openai.api_key = values["key"]
    keyA = "- " + element + " -"
    window[keyA].update("")
    values[keyA] = ""
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
    
    output = output.partition('\n')[0]
    
    print("generated value: " + output)
    
    window[keyA].update(output)
    values[keyA] = output
    
    character = regenerateCharacter()
   
def generateBio():
    openai.api_key = values["key"]
    character = regenerateCharacter()
    prompt = character + "Write a short but sweet summary/biography about the character:"
    # model_inputs = { "text": prompt, "length": 128, "temperature": 0.75, "topK": 50, "topP":1 }
            
    print("generating biography...")
    
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
    
    print("finished, with length of " + str(len(output)) + " characters.")
    
    window["- Bio/Summary -"].update(output)
    values["- Bio/Summary -"] = output
    
    character = regenerateCharacter()
           
# helper function to quickly print the character
def printCharacter():
    print("----------- CHARACTER ---------------")
    print(character)
    print("-------------------------------------")
    
def askQuestion():
    character = regenerateCharacter()
    prompt = "a conversation with the following character:\n" + character + "\nQ: " + values["question"] + "\n" + values["- Name -"] + ":"
    print(prompt)
    # model_inputs = { "text": prompt, "length": 128, "temperature": 0.75, "topK": 50, "topP":1 }
            
    print("generating biography...")
    openai.api_key = values["key"]
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=prompt,
      temperature=1.0,
      max_tokens=128,
      top_p=1,
      frequency_penalty=0.7,
      presence_penalty=0.5,
      stop=["Q:"],
    )
    
    output =  values["- Name -"]+": "+response['choices'][0]['text'].strip()
    
    print("finished, with length of " + str(len(output)) + " characters.")
    
    window["answer"].update(output)
    values["answer"] = output
    
    character = regenerateCharacter()

def save():
    Files = [('Character', '*.character')]
    file = tk.filedialog.asksaveasfile(filetypes = Files, defaultextension = Files)
    print("saved...")
    dir = file.name
    print("generating character...")
    character = regenerateCharacter() + "Bio/Summary: " + values["- Bio/Summary -"]
    print("writing...")
    with open(dir, 'w') as f:
        f.write(character)
    print("done")

def load():

    Files = [('Character', '*.character')]
    file = tk.filedialog.askopenfile(filetypes = Files)
    dir = file.name
    
    print("begin loading...\n===============")
    
    with open(dir, 'r') as f:
        text = f.readlines()
    for x in text:
        att = x.split(":", 1)
        if len(att) != 1:
            print("found " + att[0] + ", loading value...")
            keyA = "- " + att[0] + " -"
            window[keyA].update(att[1].strip())
            values[keyA] = att[1].strip()
    
    
    print("===============\ndone!") 

# Create the window 
window = sg.Window("Demo", layout, font=("Helvetica",10))

# Create an event loop
while True:
    event, values = window.read()
    # program goes here
    if event == "Bio/Summary":
        generateBio()
    elif event == "Export":
        save()
    elif event == "Import":
        load()
    elif event == "Ask":
        askQuestion()
    else:
        generateValue(event)
    
    
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

window.close()