import pathlib
import time

import PySimpleGUI as sg


sg.theme('DarkBrown1')
path = pathlib.Path('user_set.txt')


def set_time():
    layout = [[sg.Text('タイマーの時間の設定', size=(None, 2))],
              [sg.Spin([m for m in range(61)], size=2, font=(None, 15)), sg.T('分'),
               sg.Spin([s for s in range(60)], size=2, font=(None, 15)), sg.T('秒')],
              [sg.VPush()],
              [sg.Checkbox('デフォルトとして設定する', key='-DEFAULT-')],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('タイマーの設定', layout, size=(250, 160), element_justification='center')

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'キャンセル':
        user = (0, 0)
    elif event == 'OK':
        user = (values[0], values[1])
        if values['-DEFAULT-']:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f'{values[0]} {values[1]}')
    window.close()
    return user


def main():
    started = False
    if path.exists():
        with open(path, encoding='utf-8') as f:
            user_min, user_sec = map(int, f.read().split())
    else:
        user_min, user_sec = (0, 0)

    current_min, current_sec = user_min, user_sec

    layout = [[sg.T(f'{current_min:02d} : {current_sec:02d}', pad=(None, 10), font=(None, 35), key='-DISPLAY-')],
              [sg.VPush()],
              [sg.B('スタート'), sg.B('ストップ'), sg.B('リセット')],
              [sg.B('設定'), sg.B('閉じる')]]

    window = sg.Window('タイマー', layout, size=(280, 150), element_justification='center')

    def update_display():
        window['-DISPLAY-'].update(f'{int(current_min):02d} : {int(current_sec):02d}')

    while True:
        event, _ = window.read(timeout=50)
        if event == sg.WIN_CLOSED or event == '閉じる':
            break

        elif event == 'スタート':
            if not started:
                started = True
                end_time = time.time() + current_min*60 + current_sec
        elif event == 'ストップ':
            started = False
        elif event == 'リセット':
            started = False
            current_min, current_sec = user_min, user_sec
            update_display()
        elif event == '設定':
            started = False
            user_min, user_sec = set_time()
            current_min, current_sec = user_min, user_sec
            update_display()

        if started:
            remaining_time = end_time - time.time()
            if remaining_time < 0:
                sg.popup('時間になりました', keep_on_top=True)
                started = False
                current_min, current_sec = user_min, user_sec
            else:
                current_min, current_sec = divmod(remaining_time, 60)
            update_display()

    window.close()


if __name__ == '__main__':
    main()
