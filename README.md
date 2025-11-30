# AIAnalysis1
Practice project for a gen-AI interface, with interview transcript analysis in mind.

The files are for a Flash app, running on Heroku here: https://testappai0-e16cf7da4690.herokuapp.com (depending on the version I'm working on - it might require your own API credentials or an access code, or it might just run out of resources at some point). It's mainly designed to use a gen AI model to analyze data like interview transcripts, but it's abstracted into general "definitions", "data", and "queries" components. These components are added to a conversation history with some text added to the prompt to specify what they're to be used for.

It also has an optional "Thomas" mode if you want to risk getting my personal opinions.

Example:

Definitions: Define a code as a concept that appears at multiple points in the text, where it has a similar meaning but possibly different wording; the code is labeled as the abstracted meaning of the text. A code should have a specific valence - use different codes for positive and negative attitudes towards similar concepts.

Data: The following text contains interview transcripts. The symbol ### indicates where a new participant transcript begins. The participant identifier is given after the ### symbol. ### Participant 1. I like oranges, but not pears. ### Participant 2. I like apples, but not pears. ### Participant 3. I dislike apples and pears.

Query: Identify codes for the responses for each participant. Using the codes for analysis, what attitudes do the participants express? Create a table with a row per participant and a column per code, and set the value of each element to 1 if the participant expressed the code and 0 otherwise.

