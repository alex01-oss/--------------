import PySimpleGUI as sg

def results_page(results):
  sg.theme('DarkTeal10')

  question_layouts = []
  for result in results:
    question_layouts.append(f"Питання: {result['question']}\n")
    question_layouts.append(f"Правильна відповідь: {result['correct_answer']}\n")
    question_layouts.append(f"Ваша відповідь: {result['selected_answer']}\n")
    question_layouts.append("-" * 50 + "\n")

  layout = [
    [sg.Text('Результати тесту', font='Helvetica 16', justification='center')],
    [sg.Multiline(''.join(question_layouts), size=(50, 10), font='Verdana 11', disabled=True)],
    [sg.Button('Закрити')]
  ]

  window = sg.Window('Результати', layout, font='Verdana 11')

  while True:
    event, _ = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Закрити':
      break

  window.close()