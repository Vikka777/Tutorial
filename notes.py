class Assistant:
    def __init__(self):
        self.notes = []

    def add_note(self, note_text): #зберігає нотатки з текстовою інфою
        self.notes.append({"text": note_text})

    def search_notes(self, keyword): #проводить пошук за нотатками
        matching_notes = []
        for note in self.notes:
            if keyword in note["text"] or keyword in note["tags"] or keyword in note["keywords"]:
                matching_notes.append(note)
        return matching_notes

    def edit_note_text(self, note_index, new_text): #редагує нотатки
        if note_index < len(self.notes):
            self.notes[note_index]["text"] = new_text
            return True
        return False

    def delete_note(self, note_index): #видаляє нотатки
        if note_index < len(self.notes):
            del self.notes[note_index]
            return True
        return False

    #додає в нотатки "теги" ключові слова, що описують тему та предмет запису
    def add_tags_to_note(self, note_index, tags):
        if note_index < len(self.notes):
            self.notes[note_index]["tags"].extend(tags)
            return True
        return False

if __name__ == "__main__":
    assistant = Assistant()