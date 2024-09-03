from boggle_tracker.outputs.base_output import BaseOutput
from boggle_tracker.outputs.stdout_output import StdoutOutput
from boggle_tracker.outputs.rich_output import RichOutput


class OutputFactory:
    @staticmethod
    def create(output_type: str) -> BaseOutput:
        if output_type == "stdout":
            return StdoutOutput()
        elif output_type == "rich":
            return RichOutput()
        else:
            raise ValueError(f"Unsupported output type: {output_type}")
