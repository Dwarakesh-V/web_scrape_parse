from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize

with open("sections_site.txt") as f:
    content = f.read().split("\n\n")

nc=[]
for i in content:
    nc.append(i.split("\n")[0])

newcon=content.copy()
content=nc

all_MiniLM_L12_v2 = SentenceTransformer("all-MiniLM-L12-v2")
encoded_content = all_MiniLM_L12_v2.encode(content,convert_to_tensor=True)

# uip = input("Enter query: ")
uip = ["price","brand","related items","mrp"]
enc_ui = [all_MiniLM_L12_v2.encode(i,convert_to_tensor=True) for i in uip]

for e,enc_ip in enumerate(enc_ui):
    mc=(0,-1) # min of cos
    # enc_ip = all_MiniLM_L12_v2.encode(convert_to_tensor=True)
    for i,sc in enumerate(encoded_content):
        score=util.cos_sim(sc,enc_ip).item()
        if score>mc[1]:
            mc=(i,score)
        # print(score, content[i][:80])

    print(f"\n\n---break---\n\nQuery: {uip[e]}\nContent: {newcon[mc[0]]}\nConfidence: {mc[1]}")
