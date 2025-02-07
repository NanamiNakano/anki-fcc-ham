import genanki
import json


class MyNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


with open("templates/front.html", "r") as f:
    front_template = f.read()

with open("templates/back.html", "r") as f:
    back_template = f.read()

with open("templates/style.css", "r") as f:
    style_css = f.read()

fcc_model = genanki.Model(
    1779498341,
    "FCC Amateur Radio Exam",
    fields=[
        {"name": "ID"},
        {"name": "Question"},
        {"name": "option_1 (A)"},
        {"name": "option_2 (B)"},
        {"name": "option_3 (C)"},
        {"name": "option_4 (D)"},
        {"name": "Answer"},
        {"name": "Description"},
    ],
    templates=[
        {
            "name": "FCC Amateur Radio Exam",
            "qfmt": front_template,
            "afmt": back_template,
        },
    ],
    css=style_css,
)

my_deck = genanki.Deck(
    2122706713,
    "FCC Amateur Radio Exam Technician (2022-2026)",
)

my_deck.add_model(fcc_model)


with open("parsed/technican.json", "r") as f:
    data = json.load(f)

for question in data:
    my_deck.add_note(
        MyNote(
            model=fcc_model,
            fields=[
                question["id"],
                question["question"],
                question["answers"][0],
                question["answers"][1],
                question["answers"][2],
                question["answers"][3],
                question["correct"],
                question["description"],
            ],
        )
    )

genanki.Package(my_deck).write_to_file("output.apkg")
