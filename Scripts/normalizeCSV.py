from tempfile import NamedTemporaryFile
import shutil
import csv

filename = '../PhotographyStyleAnalysis/input/movie-classifier/Multi_Label_dataset/label_studio_200_images.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)
fields = ['image', 'id', 'Color', 'Palette', 'DoF', 'Composition', 'Type', 'annotator', 'annotation_id', 'created_at', 'updated_at', 'lead_time']

# iterate over each line as a ordered dictionary and print only few column by column name
with open(filename, 'r') as read_obj, tempfile:
    csv_dict_reader = csv.DictReader(read_obj, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields)
    writer.writeheader()
    header_mapping = next(csv_dict_reader)
    for row in csv_dict_reader:
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
        writer.writerow(row)

shutil.move(tempfile.name, filename)