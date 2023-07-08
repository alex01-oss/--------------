import PySimpleGUI as sg
from test import test_page
import glob
import json

sg.theme('DarkTeal10')

def is_valid_json(file_path):
  try:
    with open(file_path) as f:
      json.load(f)
      return True
  except (FileNotFoundError, json.JSONDecodeError):
    return False

def main():
  files = glob.glob('*/*.json')
  names = [file.split('.')[0].replace('json\\', '') for file in files if is_valid_json(file)]

  layout = [
    [sg.Text('Тестування')],
    [sg.Listbox(names, key='-listbox-', size=(32, 4))],
    [sg.Button('Вибрати')]
  ]
  window = sg.Window('Тестування', layout, size=(400, 180), font='Helvetica 14')

  while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
      break
    if event == 'Вибрати':
      selected_page = values['-listbox-'][0] if values['-listbox-'] else None
      if selected_page:
        test_name = selected_page.split('.')[0]
        test_page(test_name)

  window.close()

if __name__ == '__main__':
  main()