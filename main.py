import kivy
import chatbot

from strings import Strings

kivy.require('2.0.0')
from kivy.app import App


class EllisApp(App):
    def build(self):
        mylabel = self.root.ids.my_label
        welcome= Strings.emmaTag + chatbot.greetAtStart() + Strings.tellName
        mylabel.text = welcome

    def display(self):

        mytextinput = self.root.ids.my_textinput
        user_input=mytextinput.text
        mylabel = self.root.ids.my_label
        mytextinput.text = ""

        global correctNameGiven
        global count

        """ get response from chatbot """
        output = chatbot.chat(user_input,correctNameGiven)

        """
        To check whether user has given his name
        """
        if(output==-1):
            count+=1
            if(count<3):
                output = Strings.invalidName
            else:
                output = Strings.notTalkFurther
        else:
            correctNameGiven = True

        mylabel.text += Strings.you + user_input + "\n"+ Strings.emmaTag + output + "\n\n"


if __name__ == "__main__":
    correctNameGiven=False
    count=0
    EllisApp().run()