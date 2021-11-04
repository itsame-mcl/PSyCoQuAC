from asciimatics import Frame, Layout, TextBox, Button
from asciimatics.screen import Screen

class FrameConnexion(Frame):

    def __init__(self, screen : Screen, model):
        super(FrameConnexion, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3,
                                                    hover_focus = Tr, title = ("Agent "+str(agent.agent_id)))
        # Save off the model that accesses the contacts database.
        self._model = model

        # Creation des deux TextBox pour rensiegner son nom d'utilisateur et son mot de passe.
        layout = Layout([100], fill_frame = True)
        self.add_layout(layout)
        layout.add_widget(TextBox(1, label = "Nom d'utilisateur :", as_string = True))
        layout.add_widget(TextBox(1, label = "Mot de passe :", as_string=True, on_change = ))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(FrameConnexion, self).reset()
        self.data = self._model.get_current_contact()

    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")