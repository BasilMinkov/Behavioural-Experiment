import random
from expyriment import design, control, stimuli, io, misc
from prepare_dataset import prepare_phrases, prepare_instruction

# Prepare stimuli
phrases = prepare_phrases()
instruction = prepare_instruction()

# Set mode for convenient development
# control.set_develop_mode(True)

# Define variables
response_keys = [misc.constants.K_UP, misc.constants.K_DOWN]  # left and right arrow keys for responses
random_colour = [misc.constants.C_BLUE, misc.constants.C_GREEN]  # green or blue colour for last stimuli

# Create and initialize an Experiment
exp = design.Experiment("The Influence Of Emotions")
control.initialize(exp)

# Define and preload standard stimuli
fixcross = stimuli.FixCross()
fixcross.preload()

# Initialise block
block = design.Block(name="Block 1")

# Create design
for i in range(len(phrases)):

    # Initialise trail
    trial = design.Trial()

    # Initialise first stimuli: a phrase to be presented by words.
    stim = stimuli.TextLine(text=phrases[i][0], text_colour=misc.constants.C_WHITE)
    stim.preload()
    trial.add_stimulus(stim)

    # Initialise second stimuli: a phrase to be presented at once.
    splitted_phrase2 = phrases[i][1].split()
    for word in splitted_phrase2:
        stim = stimuli.TextLine(text=word, text_colour=misc.constants.C_WHITE)
        stim.preload()
        trial.add_stimulus(stim)
    current_colour = random.randint(0, 1)
    stim = stimuli.TextLine(text=splitted_phrase2[-1], text_colour=random_colour[current_colour])
    stim.preload()
    trial.add_stimulus(stim)
    trial.set_factor("Colour", current_colour)

    if phrases[i][2] is not None:
        stim = stimuli.TextLine(text=phrases[i][2], text_colour=misc.constants.C_WHITE)
        stim.preload()
        trial.add_stimulus(stim)
        trial.set_factor("Question", True)
    else:
        trial.set_factor("Question", False)

    block.add_trial(trial)

# Shuffle trails
block.shuffle_trials()
exp.add_block(block)

# Set data variable names
exp.data_variable_names = ["Colour", "Trial", "Key Stimulus", "RT Stimulus", "Key Question", "RT Question"]
# exp.misc.data_preprocessing.write_csv_file(["Colour", "Block", "Trial", "Key Stimulus", "RT Stimulus", "Key Question",
#                                             "RT Question"])

if __name__ == "__main__":

    # Run experiment
    control.start()

    # Enter first block of the experiment.
    for block in exp.blocks:
        # Show instruction.
        stimuli.TextScreen("Инструкция", instruction).present()
        exp.keyboard.wait()
        for trial in block.trials:

            # Present the first phrase (5s).
            trial.stimuli[0].present()
            exp.clock.wait(5000)

            # Present the fixation cross (500 ms).
            fixcross.present()
            exp.clock.wait(500)

            # Present all the words (300 ms) and fixation dots (200 ms) in second phrase.
            if trial.get_factor("Question"):
                # Finally ask question in this case.
                for stimulus in trial.stimuli[1:-3]:
                    stimulus.present()
                    exp.clock.wait(300)
                    fixcross.present()
                    exp.clock.wait(200)

                # Present the last word (500 ms).
                trial.stimuli[-3].present()
                exp.clock.wait(500)

                # Present the last coloured word until the buttonpress.
                trial.stimuli[-2].present()
                key1, rt1 = exp.keyboard.wait(response_keys)

                # Present the question until the answer is given.
                trial.stimuli[-1].present()
                key2, rt2 = exp.keyboard.wait(response_keys)

                # Save the results to the data file.
                exp.data.add([trial.get_factor("Colour"), trial.id, key1, rt1, key2, rt2])
                # exp.misc.data_preprocessing.write_csv_file([trial.get_factor("Colour"), trial.id, key1, rt1, key2, rt2])

            else:
                for stimulus in trial.stimuli[1:-2]:
                    stimulus.present()
                    exp.clock.wait(300)
                    fixcross.present()
                    exp.clock.wait(200)

                # Present the last word (500 ms).
                trial.stimuli[-2].present()
                exp.clock.wait(500)

                # Present the last coloured word until the buttonpress.
                trial.stimuli[-1].present()
                key1, rt1 = exp.keyboard.wait(response_keys)

                # Save the results to the data file.
                exp.data.add([trial.get_factor("Colour"), trial.id, key1, rt1])

    control.end()
