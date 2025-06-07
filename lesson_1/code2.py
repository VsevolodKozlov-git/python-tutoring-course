friends = ['anton', 'seva', 'igor', 'serega']

for friend in friends:
    if friend == 'seva':
        continue

    if friend.startswith('s'):
        print(f'{friend}, твое имя начинается также как у меня!')
