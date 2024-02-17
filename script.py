import npyscreen
import subprocess

class GitApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", GitForm, name="Git Console")

class GitForm(npyscreen.FormBaseNew):
    def create(self):
        # Define the layout grid
        y, x = self.useable_space()
        commit_field_height = 5
        button_width = 15

        # Add the commit field
        self.commit_field = self.add(npyscreen.TitleText, name="Commit Message:", begin_entry_at=20, rely=2, max_height=commit_field_height)

        # Add the buttons horizontally
        button_x = x // 2 - (button_width + 2) * 2
        self.add_button = self.add(npyscreen.ButtonPress, name="Git Add", relx=button_x, rely=7, width=button_width, when_pressed_function=self.git_add)
        self.commit_button = self.add(npyscreen.ButtonPress, name="Git Commit", relx=button_x + button_width + 2, rely=7, width=button_width, when_pressed_function=self.git_commit)
        self.pull_button = self.add(npyscreen.ButtonPress, name="Git Pull", relx=button_x, rely=8, width=button_width, when_pressed_function=self.git_pull)
        self.push_button = self.add(npyscreen.ButtonPress, name="Git Push", relx=button_x + button_width + 2, rely=8, width=button_width, when_pressed_function=self.git_push)

        # Add a text box for output
        self.output_area = self.add(npyscreen.BoxTitle, name="Output:", relx=2, rely=10, max_height=y - 13, max_width=x - 4, editable=False)

    def execute_git_command(self, command):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip() + "\n" + result.stderr.strip()
        self.output_area.entry_widget.values = output.splitlines()
        self.output_area.entry_widget.display()

    def git_add(self):
        commit_message = self.commit_field.value
        if commit_message:
            self.execute_git_command(["git", "add", "."])
            npyscreen.notify_confirm("Files added to staging area.", "Git Info")

    def git_commit(self):
        commit_message = self.commit_field.value
        if commit_message:
            self.execute_git_command(["git", "commit", "-m", commit_message])
            npyscreen.notify_confirm("Commit created.", "Git Info")

    def git_pull(self):
        self.execute_git_command(["git", "pull"])
        npyscreen.notify_confirm("Pull operation completed.", "Git Info")

    def git_push(self):
        commit_message = self.commit_field.value
        if commit_message:
            self.execute_git_command(["git", "commit", "-m", commit_message])
            self.execute_git_command(["git", "push"])
            npyscreen.notify_confirm("Commit and push operations completed.", "Git Info")

if __name__ == "__main__":
    app = GitApp()
    app.run()
