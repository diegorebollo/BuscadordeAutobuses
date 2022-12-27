import json


def cleaning_days(data):

    diario = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    diario_sabado = ['Lunes', 'Martes',
                     'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    semanal = ['Lunes', 'Martes', 'Miércoles',
               'Jueves', 'Viernes', 'Sábado', 'Domingo']

    dias_cleaned = []

    for dias in data:
        temp_list = []
        for dia in dias:
            if dia == 'L':
                temp_list.append('Lunes')
            elif dia == 'M':
                temp_list.append('Martes')
            elif dia == 'X':
                temp_list.append('Miércoles')
            elif dia == 'J':
                temp_list.append('Jueves')
            elif dia == 'V':
                temp_list.append('Viernes')
            elif dia == 'S':
                temp_list.append('Sábado')
            elif dia == 'D':
                temp_list.append('Domingo')

        if temp_list == diario:
            temp_list.append('De Lunes a Viernes')
        elif temp_list == diario_sabado:
            temp_list.append('De Lunes a Sábado')
        elif temp_list == semanal:
            temp_list.append('De Lunes a Domingo')
        elif len(temp_list) == 6 and 'Lunes' in temp_list and 'Viernes' in temp_list:
            temp_list.append(f'De Lunes a Viernes y {temp_list[-1]}s')
        elif len(temp_list) == 2 and temp_list[0] != temp_list[1]:
            temp_list.append(f'{temp_list[0]}s y {temp_list[1]}s')
        elif len(temp_list) == 4 and 'Lunes' in temp_list and 'Jueves' in temp_list:
            temp_list.append('De Lunes a Jueves')

        dias_cleaned.append(temp_list)

    return json.dumps(dias_cleaned)
