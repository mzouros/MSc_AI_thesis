from tempfile import NamedTemporaryFile
import shutil
import csv
import numpy as np
import pandas as pd

filename = '../PhotographyStyleAnalysis/input/movie-classifier/Multi_Label_dataset/Tasks/label_studio_200_images.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)
fields = ['image', 'id', 'Color', 'Palette', 'DoF', 'Composition', 'Type', 'annotator', 'annotation_id', 'created_at', 'updated_at', 'lead_time']

dataPal = np.array([['image', 'Palette']])
dataComp = np.array([['image', 'Composition']])
dataType = np.array([['image', 'Type']])

# Transform initial Label Studio .csv file (fix ids, remove extra strings, 0-1 bool for binary tasks)
with open(filename, 'r') as read_obj, tempfile:
    csv_dict_reader = csv.DictReader(read_obj, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields)
    writer.writeheader()
    header_mapping = next(csv_dict_reader)
    for row in csv_dict_reader:
        # fix ids
        id = row['image'].split("photo")[1]
        row['image'] = "photo"+id
        # remove extra strings
        if "choices" in row['Palette']:
            row['Palette'] = row['Palette'].split(": ")[1].replace('}', '')
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "choices" in row['Composition']:
            row['Composition'] = row['Composition'].split(": ")[1].replace('}', '')
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "choices" in row['Type']:
            row['Type'] = row['Type'].split(": ")[1].replace('}', '')
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "Deep" in row['DoF']:
            row['DoF'] = "Deep"
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "Shallow" in row['DoF']:
            row['DoF'] = "Shallow"
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        # Color binary classification task
        color = row['Color']
        if color == "Colorful":
            row['Color'] = 1
        else:
            row['Color'] = 0
        # DoF binary classification task
        dof = row['DoF']
        if dof == "Deep":
            row['DoF'] = 1
        else:
            row['DoF'] = 0

        # keep info to create new .csv files for the multi-label tasks
        dataPal = np.append(dataPal, np.array([[row['image'], row['Palette']]]), axis=0)
        dataComp = np.append(dataComp, np.array([[row['image'], row['Composition']]]), axis=0)
        dataType = np.append(dataType, np.array([[row['image'], row['Type']]]), axis=0)

        writer.writerow(row)

shutil.move(tempfile.name, filename)

# Create new .csv files for the multi-labeled tasks (Palette, Composition, Type)
def wrap_eval(x):
    try:
        return eval(x)
    except:
        return [x]

dataFrames = [dataPal, dataComp, dataType]
csvNames = ['palette.csv', 'composition.csv', 'type.csv']
colOfInterest = ['Palette', 'Composition', 'Type']
for j in range(3):
    df = pd.DataFrame(dataFrames[j])
    df.to_csv(csvNames[j], header=None, index=False)
    df = pd.read_csv(csvNames[j])
    df[colOfInterest[j]] = df[colOfInterest[j]].apply(wrap_eval)
    for i, row in df.iterrows():
        for colour in row[colOfInterest[j]]:
            try:
                df[colour]             # (1) in the steps above.
            except:
                df[colour] = 0         # (2)
            finally:
                df.loc[i, colour] = 1  # (3)

    fixed = pd.DataFrame(df)
    fixed.to_csv(csvNames[j], index=False)