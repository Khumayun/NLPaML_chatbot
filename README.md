# NLPaML_chatbot

### Configuration

- Python 3.10.2

### Hidden pitfalls

We have found that converting directly from RST can lead to numerous errors due to\
its impossible to define in json some keys, that are manually defined by developer of a library\
in other words, only after building the rst files we can extract those keys. To do so,\
we can use html builder or xml builder. Its common practice to parse html using bs4 to \
extract text but in our case its inefficient, so we make use of xml builder.

The workflow to build a **valid** xml file from rst using sphinx is as follows:

- place rst files in `docs/src`
- run `sphinx-build -b xml docs/src/ docs/build/xml/`
- for the generated files, using regex remove links of the format
`<reference><literal>the_text</literal></reference>`,\
because it creates separate dict for a link and removes the_text
- put the xml files in data folder
- run parser `python data_converter/module/parse.py path/to/input.xml path/to/output.json`\
or use runner function in data_converter/src/parse.py
