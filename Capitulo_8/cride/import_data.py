import csv
from cride.circles.models import Circle
archivo_csv = 'circles.csv'
with open(archivo_csv, 'r') as file:
    lector_csv = csv.DictReader(file)
    for fila in lector_csv:
        circle = Circle(
            name=fila['name'],
            slug_name=fila['slug_name'],
            is_public=bool(int(fila['is_public'])),
            verified=bool(int(fila['verified'])),
            members_limit=int(fila['members_limit'])
        )
        circle.save()
