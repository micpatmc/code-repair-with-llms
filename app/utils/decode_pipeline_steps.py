from typing import List

def decode_pipeline_steps(pipeline_binary: int) -> List[int]:
    '''
    Decodes the binary representation of pipeline steps into a list of step indices.
    For example: binary 21 (0b10101) -> [1, 3, 5]

    Parameters:
    - pipeline_binary int: Binary representation of selected pipeline steps

    Returns:
    - List[int]: Indices of the selected pipeline steps (1-based)
    '''
    steps = []
    for i in range(6):  # Assuming 6 pipeline steps
        if pipeline_binary & (1 << i):
            steps.append(i + 1)  # Convert 0-based to 1-based index
    return steps