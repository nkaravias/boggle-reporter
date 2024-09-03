from boggle_tracker.outputs.base_output import BaseOutput
from boggle_tracker.outputs.stdout_output import StdoutOutput


class OutputFactory:
    @staticmethod
    def create(output_type: str) -> BaseOutput:
        if output_type == 'stdout':
            return StdoutOutput()
        else:
            raise ValueError(f"Unsupported output type: {output_type}")
