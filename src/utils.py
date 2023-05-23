import openai
import difflib

prompts_to_fill = [
    {'summarize': """
You will be provided with text delimited by triple quotes.

Summarize the text by extracting the most relevant information in the form of bullet points.

\"\"\"{}\"\"\"
"""},   
    {'rewrite': """
You will be provided with text delimited by triple quotes.

Rewrite the text taking into account the following information:
{}
\"\"\"{}\"\"\"
"""},
    {'spellcheck': """
You will be provided with text delimited by triple quotes.
If the text contains spell or grammar errors provide the text corrected.

If the text does not contain errors return back the text delimited by triple quotes.

\"\"\"{}\"\"\"
"""}
]


def define_prompt(action, input_text, text_goals=False):
    prompt = ''

    if action == 'summarize':
        prompt = prompts_to_fill[0]['summarize'].format(input_text)
    elif action == 'rewrite':
        prompt_config = paraphrase_prompt(text_goals)
        prompt = prompts_to_fill[1]['rewrite'].format(prompt_config, input_text)
    elif action == 'spellcheck':
        prompt = prompts_to_fill[2]['spellcheck'].format(input_text)

    return prompt


def model_request(model, prompt, temp=0):
    
    r = openai.ChatCompletion.create(
        model=model,
        messages=[{
        'role':'system', 'content':"You are an expert proofreader, the most advanced AI tool on the planet.",
        'role':'user', 'content': prompt}],
        temperature=temp)
    
    return r.choices[0]['message']['content']


goals_prompts = {
    'audience' : "audience is {}\n",
    'formality' : "{} tone\n",
    'domain' : '{}\n',
    'intent' : 'intent to {}\n',
    'style' : 'in the style of "{}" \n'
}


def paraphrase_prompt(text_goals):

    prompt_parameters = []
    for key, value in text_goals.items():
        if key == 'style':
            if value != '':
                prompt_parameters.append(goals_prompts[key].format(value))
        elif value != 'Select an option':
            prompt_parameters.append(goals_prompts[key].format(value))

    if len(prompt_parameters) == 0:
        prompt_config = 'it is easier to understand\navoid repetitions of words and phrases\n'
    else:
        prompt_config = ''.join(prompt_parameters) 
            
    return prompt_config


def correction_style(word, correction):
    html_correction = """<abbr style="text-decoration: none"  title="{}">\
<mark style="background-color: #afa">{}</mark></abbr>"""
    return html_correction.format(word.replace('-',''), correction.replace('+',''))


def compare_texts(text_input, text_corrected):

    text_corrected = text_corrected.replace('"', '')
    d = difflib.Differ()
    diff = d.compare(text_input.split(), text_corrected.split())
    list_words = [word for word in diff  if '?' not in word]
    
    reviewed_sentence = []
    correction_word = False
    for idx, word in enumerate(list_words):
        if correction_word:
            correction_word=False
            pass
        elif '-' in word and '+' in list_words[idx+1]:
            correction_word=True
            reviewed_sentence.append(correction_style(word, list_words[idx+1]))
        else:
            reviewed_sentence.append(word)

    return ''.join(reviewed_sentence)


