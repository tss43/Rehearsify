# Rehearsify - an app for practising foreign language words

## Overview

Rehearsify is an app for practising foreign language words. To get started, these can be loaded in from a simple .txt file. This allows the user great flexibility in the questions they want to practise and the corresponding answers that will be counted as correct. Access is provided through a simple, intuitive GUI, from which progress scores might be saved. Further offered functionality includes the option to look up the appropriate answer for a question or vice versa, and to inspect some overall statistics of the the loaded dictionary of translations.

## Usage

The best way to access the GUI is to call it from the command line by invoking `python main.py`, or its simpler alias `Rehearsify`. This will open the initial screen: ![Initial screen](./docs/Initial_screen.png) Clicking the `Open file` button spawns a file explorer with which a file can be selected for opening. Currently supported file formats are:

- .txt: for supplying a _new_ translation dictionary to practise. Every line, representing a single translation, should be of the form 'question1'; 'question2'; ... = 'answer1', 'answer2', answer', ...
- .csv, .xls(x) and .pkl: for continuing with statistics of last practise session

After opening a translation dictionary file, the GUI window will look like: ![Opened file screen](./docs/Opened_file_screen.png) Here, the user will be prompted with a randomly selected question (weighted by the percentage of wrong attempts) to rehearse. Upon typing an answer in the user response field and pushing the `Go` button, or simply pressing `Enter`, it will be checked against the correct answer on record in the dictionary and the statistics are updated correspondingly. The correct answer, and if the supplied user answer coincided, is shown to the user in the lower pane log: ![Answered questions screen](./docs/Answered_questions_screen.png) Note that practise statistics and the user answer become visible upon maximising the window: ![Answered questions screen (maximised)](./docs/Answered_questions_screen_maximised.png)  

- save as -> file formats

- .txt: for saving as plain list of translations, without statistics
- .csv, .xls(x) and .pkl: for saving dictionary as tabular data, including statistics of practise session

- ordering string + screen shot
- update with -> use more actual .txt to add new translations and remove those not .txt

- lookup buttons + screen shot
- dict statistics button + screen shot

Finally, some further command line functionality to query a translation dictionary is also provided:

```bash
FindDuplicates translation_dictionary_fpath
Statistics translation_dictionary_fpath
```

![Dictionary statistics screen](./docs/Dictionary_statistics_screen.png)
![Example dictionary txtfile screen](./docs/Example_dictionary_txtfile.png)
![Ignore str in sorting screen](./docs/Ignore_str_in_sorting_screen.png)

![Lookup screen](./docs/Lookup_screen.png)
![Save file screen](./docs/Save_file_screen.png)

## TO-DO

- [x] write tests
- [ ] write README.md
- [ ] Make Github Project public
- [ ] Add delight to the experience when all tasks are complete :tada:

<!-- comments -->
