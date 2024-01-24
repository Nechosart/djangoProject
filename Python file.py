import logging

logging.basicConfig(filename='file.log', filemode='a', level=logging.DEBUG,
                    format='Error:%(asctime)s %(levelname)s %(message)s')

step = 1
number = 0
do = 1
text = ['enter the first number', '1 - clear, 2 - plus, 3 - minus, 4 - multiplication, 5 - divide', '1 - clear, - enter',
        'enter the second number']

while True:
    a = input(text[step])
    logging.info(f'{text[step]} Entered: {a}')
    if a == '1':
        step = 1
    else:
        if step == 1 or step == 3:
            try:
                number1 = int(a)
            except ValueError:
                step -= 1
                logging.exception('Not number')
        elif step == 3:
            try:
                number = int(a)

            expect V


        step += 1


try:
    a = int(input())
    print(10/a)

except ZeroDivisionError:
    logging.exception('dividing by 0')
except ValueError:
    logging.exception('dividing by string')
else:
    logging.info('Everything is good:D')

