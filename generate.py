import genanki
import json
import os

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
        {"name": "Figure"},
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

technician_deck = genanki.Deck(
    2122706713,
    "FCC Amateur Radio Exam Technician (2022-2026)",
)

general_deck = genanki.Deck(
    1940122975,
    "FCC Amateur Radio Exam General (2023-2027)",
)

extra_deck = genanki.Deck(
    2115817860,
    "FCC Amateur Radio Exam Extra (2024-2028)",
)

decks = [technician_deck, general_deck, extra_deck]
classes = ["technician", "general", "extra"]
figures = os.listdir("assets/")

for deck, class_ in zip(decks, classes):
    deck.add_model(fcc_model)

    with open(f"parsed/{class_}.json", "r") as f:
        data = json.load(f)

    for question in data:
        if question["figure"] == "":
            figure = ""
        else:
            figure = f'<img src="{question["figure"]}.png">'
        deck.add_note(
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
                    figure,
                ],
            )
        )

    package = genanki.Package(deck)
    package.media_files = map(lambda x: f"assets/{x}", list(filter(lambda x: x[0] == class_[0], figures)))
    package.write_to_file(f"out/{class_}.apkg")