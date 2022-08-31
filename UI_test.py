import PySimpleGUI as sg


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

element = [[sg.Text("Name"), sg.Input(), sg.Button("Generate")]]

layout = [[sg.Menu(menu_def)], [sg.Column(element)] ]

# layout end ------

# Create the window 
window = sg.Window("Demo", layout, font=("Helvetica",10))

# Create an event loop
while True:
    event, values = window.read()
    # program goes here
    
    
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

window.close()