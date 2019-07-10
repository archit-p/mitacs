import re
from random import randint as ri

def flow2ngram(fp_in, fp_out, n=2):
    out_ngrams = []
    with open(fp_in, 'r') as inline:
        for line in inline:
            new_ngrams = generate_ngrams(line, n)
            out_ngrams.extend(new_ngrams)
    if(fp_in.rsplit("/")[-1][0] == 'b'):
        label = 'Benign'
    elif(fp_in.rsplit("/")[-1][0] == 'm'):
        label = 'Malware'
    else:
        label = ""

    with open(fp_out, 'w') as outfile:
        for ngram in out_ngrams:
            if(label != ""):
                outfile.write(ngram + "," + label + "\n")
            else:
                outfile.write(ngram + "\n")

def generate_ngrams(s, n):
    s = s.lower()
    output = []

    s = re.sub(r'[^a-zA-Z0-9 \s]', '', s)

    tokens = [token for token in s.split(" ") if token != " "]
    print(len(tokens))
    for i in range(len(tokens)-n):
        output.append(' '.join(tokens[i:i+n]))
    return output
