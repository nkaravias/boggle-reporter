from boggle_tracker.outputs.base_output import BaseOutput


class StdoutOutput(BaseOutput):
    def output(self, content: str):
        print(content)
