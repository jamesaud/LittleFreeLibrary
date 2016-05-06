import random
from wikiblog.models import Random_name

def generate_names_file():
    with open("nouns.txt") as nouns, open("adjectives.txt") as adjs:
        noun_lines = [noun.strip() for noun in nouns.readlines()]
        adj_lines = [adj.strip() for adj in adjs.readlines()]


    noun_length = len(noun_lines)
    adj_length = len(adj_lines) 
    unique_name_set = set()

    for i in range(10000):
        ran1 = random.randint(0,noun_length - 1)
        ran2 = random.randint(0,adj_length - 1)

        noun = noun_lines[ran1]
        adj = adj_lines[ran2]
        new_name = adj + " " + noun
        unique_name_set.add(new_name)

    with open("random_names.txt","w") as random_names:
        for name in unique_name_set:
            random_names.write(name + "\n")


def CreateNames(text_file):
    with open(text_file, 'r', encoding="ISO-8859-1") as file:
        lines = file.readlines()
    for name in lines:
        try:
            name = name.strip()
            new_random_name = Random_name(user_name=name)
            new_random_name.save()
        except:
            pass

def DeleteNames():
    for name in Random_name.objects.all():
        name.delete()

def Print100Names():
    for name in Random_name.objects.all()[:100]:
        print(name.user_name)
    print("Total Names: ", len(Random_name.objects.all()))
