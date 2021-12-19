import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# csv paths
colorCSV = pd.read_csv('../input/style-classifier/Multi_Label_dataset/Tasks/color.csv')
dofCSV = pd.read_csv('../input/style-classifier/Multi_Label_dataset/Tasks/dof.csv')
paletteCSV = pd.read_csv('../input/style-classifier/Multi_Label_dataset/Tasks/palette.csv')
compositionCSV = pd.read_csv('../input/style-classifier/Multi_Label_dataset/Tasks/composition.csv')
typeCSV = pd.read_csv('../input/style-classifier/Multi_Label_dataset/Tasks/type.csv')

######################################################### Color ########################################################
colorful = colorCSV['Colorful'].sum()
black_and_white = colorCSV['Black and White'].sum()

labels = ['Colorful', 'Black & White']
counts = np.array([colorful, black_and_white])

fig1, ax = plt.subplots(figsize=(15, 15))
y_pos = np.arange(len(labels))
ax.barh(y_pos, counts, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Counts')
ax.set_title('Color')
plt.savefig('../Plots/colorStats.png')
plt.show()
######################################################### Color ########################################################

########################################################## DoF #########################################################
deep = dofCSV['Deep'].sum()
shallow = dofCSV['Shallow'].sum()

labels = ['Deep', 'Shallow']
counts = np.array([deep, shallow])

fig2, ax = plt.subplots(figsize=(15, 15))
y_pos = np.arange(len(labels))
ax.barh(y_pos, counts, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Counts')
ax.set_title('DoF')
plt.savefig('../Plots/dofStats.png')
plt.show()
########################################################## DoF #########################################################

####################################################### Palette ########################################################
black = paletteCSV['Black'].sum()
blue = paletteCSV['Blue'].sum()
yellow = paletteCSV['Yellow'].sum()
green = paletteCSV['Green'].sum()
white = paletteCSV['White'].sum()
other = paletteCSV['Other'].sum()
gray = paletteCSV['Gray'].sum()
brown = paletteCSV['Brown'].sum()
red = paletteCSV['Red'].sum()
orange = paletteCSV['Orange'].sum()
human_skin = paletteCSV['Human Skin'].sum()
pink = paletteCSV['Pink'].sum()
violet = paletteCSV['Violet'].sum()

labels = ['Black', 'Blue', 'Yellow', 'Green', 'White', 'Other', 'Gray', 'Brown', 'Red', 'Orange', 'Human Skin',
          'Pink', 'Violet']
counts = np.array([black, blue, yellow, green, white, other, gray, brown, red, orange, human_skin, pink, violet])

fig3, ax = plt.subplots(figsize=(15, 15))
y_pos = np.arange(len(labels))
ax.barh(y_pos, counts, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Counts')
ax.set_title('Palette')
plt.savefig('../Plots/paletteStats.png')
plt.show()
####################################################### Palette ########################################################

##################################################### Composition ######################################################
undefined = compositionCSV['Undefined'].sum()
rule_of_thirds = compositionCSV['Rule of Thirds'].sum()
centered = compositionCSV['Centered'].sum()
leading_lines = compositionCSV['Leading Lines'].sum()
diagonals_and_triangles = compositionCSV['Diagonals and Triangles'].sum()
patterns_and_textures = compositionCSV['Patterns and Textures'].sum()
frame_within_frame = compositionCSV['Frame within Frame'].sum()
symmetrical = compositionCSV['Symmetrical'].sum()
minimal = compositionCSV['Minimal'].sum()
filling_the_frame = compositionCSV['Filling the Frame'].sum()

labels = ['Undefined', 'Rule of Thirds', 'Centered', 'Leading Lines', 'Diagonals and Triangles',
          'Patterns and Textures', 'Frame within Frame', 'Symmetrical', 'Minimal', 'Filling the Frame']
counts = np.array([undefined, rule_of_thirds, centered, leading_lines, diagonals_and_triangles, patterns_and_textures,
                   frame_within_frame, symmetrical, minimal, filling_the_frame])

fig4, ax = plt.subplots(figsize=(15, 15))
y_pos = np.arange(len(labels))
ax.barh(y_pos, counts, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Counts')
ax.set_title('Composition')
plt.savefig('../Plots/compositionStats.png')
plt.show()
##################################################### Composition ######################################################

######################################################### Type #########################################################
astro = typeCSV['Astro'].sum()
landscape = typeCSV['Landscape'].sum()
night = typeCSV['Night'].sum()
architectural = typeCSV['Architectural'].sum()
food = typeCSV['Food'].sum()
flora = typeCSV['Flora'].sum()
other = typeCSV['Other'].sum()
cityscape = typeCSV['Cityscape'].sum()
wildlife = typeCSV['Wildlife'].sum()
event = typeCSV['Event'].sum()
portrait = typeCSV['Portrait'].sum()
sports = typeCSV['Sports'].sum()
macro = typeCSV['Macro'].sum()
pet = typeCSV['Pet'].sum()
street = typeCSV['Street'].sum()
documentary = typeCSV['Documentary'].sum()
wedding = typeCSV['Wedding'].sum()

labels = ['Astro', 'Landscape', 'Night', 'Architectural', 'Food', 'Flora', 'Other', 'Cityscape', 'Wildlife', 'Event',
          'Portrait', 'Sports', 'Macro', 'Pet', 'Street', 'Documentary', 'Wedding']
counts = np.array([astro, landscape, night, architectural, food, flora, other, cityscape, wildlife, event, portrait,
                   sports, macro, pet, street, documentary, wedding])

fig5, ax = plt.subplots(figsize=(15, 15))
y_pos = np.arange(len(labels))
ax.barh(y_pos, counts, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Counts')
ax.set_title('Type')
plt.savefig('../Plots/typeStats.png')
plt.show()
######################################################### Type #########################################################
