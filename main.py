import tkinter
from tkinter import (
    Text, Tk, Scrollbar, BOTTOM, HORIZONTAL, FLAT, X
)
import openai as oa
from datetime import datetime as dt

oa.api_key = ''
end_reply: str = "\n\nI hope this helps! Let me know if you have any other questions.\n"
file_name = 'gpt'
quit_conditions: set = {'quit', 'q', 'end', 'stop'}


def general_purpose(data) -> str:
    prompt = f"{data}"
    language_map: dict = {
        'python': 'py',
        'javascript': 'js',
        'js': 'js',
        'html': 'html',
        'css': 'css',
        'cpp': 'cpp',
        'c++': 'cpp',
    }
    language: list = [
        key for key in language_map.keys() if key in data.lower()
    ]
    file_extension: str = language_map[language[0]] if language else 'txt'
    try:
        response: dict = oa.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=2000,
        )
    except Exception as e:
        _handle_exception(e)
        _create_gui('Error!', file_extension)

    response_list = [
        j for i in response.get("choices") for j in i.get("text")
    ]
    question_return: str = "".join(response_list).strip()
    _write_to_file(question_return, file_extension)
    print("{}{}".format(question_return, end_reply))
    _create_gui(data, file_extension)


def _create_gui(data, file_ext) -> None:
    root = Tk()
    root.title(data[:36])
    photo = tkinter.PhotoImage(file='oai.png')
    root.wm_iconphoto(False, photo)
    text = Text(
        root, font='bold', bg='#fff', fg='#000', relief=FLAT
    ) if file_ext == 'txt' else Text(
        root, wrap='none', font='bold', bg='#fff', fg='#000', relief=FLAT
    )
    text.pack(fill='both', expand=True)
    scrollbar = Scrollbar(root, orient=HORIZONTAL, command=text.xview)
    scrollbar.pack(side=BOTTOM, fill=X)
    scrollbar.config(background='#fff')
    text.config(xscrollcommand=scrollbar.set, padx=20, pady=20)

    with open('{}.{}'.format(file_name, file_ext), 'r') as file:
        if file != None:
            contents = file.read()
            text.insert('1.0', contents)
            file.close()

    root.mainloop()


def _handle_exception(e, file_extension='txt') -> str:
    print("an error occured: {}".format(e))
    e = "[{}] - {}.".format(dt.now(), e)
    _write_to_file(e, file_extension)


# TODO: Add to write file a logic that creates a folder named AI_gpt and writes the file to make home directory look cleaner
def _write_to_file(question_return, file_extension) -> None:
    with open('{}.{}'.format(file_name, file_extension), 'w') as f:
        f.write("{}\n".format(question_return))
        f.close()
    with open('gpt_database.txt', 'a') as f:
        f.write("{}\n".format(question_return))
        f.close()


def main() -> str:
    try:
        while True:
            query = input(">> ").strip()
            if query in quit_conditions:
                print('goodbye :(')
                break
            print('processing...')
            general_purpose(query)
    except Exception as e:
        _handle_exception(e)


if __name__ == "__main__":
    main()
