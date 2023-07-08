import PySimpleGUI as sg
from result import results_page
import datetime as dt
import pandas as pd
import random
import json

def save_result(user_info):
  try:
    df = pd.read_csv('result.csv')
    df.loc[len(df)] = user_info
  except FileNotFoundError:
    df = pd.DataFrame([user_info])
  df.to_csv('result.csv', index=False)

def test_page(test_name):
  sg.theme('DarkTeal10')
  with open(f'./json/{test_name}.json', 'r', encoding='utf-8') as file:
    questions = json.load(file)
  for question in questions:
    random.shuffle(question['answer_options'])

  all, score, q_index = 0, 0, 0
  current = questions[q_index]

  layout = [
    [sg.Text(current['question'], key='-question-')],
    *[[sg.Radio(option, group_id='answer', key=f'answer_{i}', default=True)]
      for i, option in enumerate(current['answer_options'])],
    [sg.Button('Наступне питання'), sg.Button('Результат', key='-result-', disabled=True)]
  ]

  window = sg.Window('Тест', layout, font='Verdana 11')
  start = dt.datetime.now()
  results = []

  while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Наступне питання':
      q_index += 1
      all += 1

      for i in range(len(current['answer_options'])):
        if values[f'answer_{i}']:
          selected = current['answer_options'][i]
          if selected == current['correct_answer']:
            score += 1
          q_result = {
            'question': current['question'],
            'correct_answer': current['correct_answer'],
            'selected_answer': selected
          }
          results.append(q_result)
          break

      if q_index < len(questions):
        current = questions[q_index]
        window['-question-'].update(current['question'])
        for i, option in enumerate(current['answer_options']):
          window[f'answer_{i}'].update(text=option)

      else:
        end = dt.datetime.now()
        time = end - start
        grade = round((score / all), 1)
        minutes, seconds = divmod(time.seconds, 60)
        sg.popup(f'Правильні відповіді: {score} / {all}\nОцінка: {grade}\nЧас проходження: {minutes:02d}:{seconds:02d}')
        user_info = {'name': sg.popup_get_text('Введіть ваше ім\'я:')}
        if user_info['name']:
          user_info.update({
            'test': test_name,
            'grade': grade,
            'time': f'{minutes:02d}:{seconds:02d}'
          })
          save_result(user_info)
          window['-result-'].update(disabled=False)

    if event == '-result-':
      results_page(results)
      window.close()

  window.close()