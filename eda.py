"""
Michelle Kim
CSE 163 AA
Exploratory data anlaysis for the Harry Potter Spells, 
Characters and Books Dataset. 
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

###EDA for Spells.csv 

def load_spells(path: str) -> pd.DataFrame:
    spells = pd.read_csv(path, sep=';', na_values = ['Unknown'])
    return spells

#How large is your dataset?
def spells_size(spells: pd.DataFrame) -> None:
    """
    prints the number of rows and columns and the column names
    """
    rows, cols = spells.shape
    print(f"Rows: {rows}, Columns: {cols}")
    print(f"Columns: {list(spells.columns)}")

#Does your dataset have any missing data?
def find_missing_spells(spells: pd.DataFrame) -> None:
    missing_per_column = spells.isnull().sum()
    print(f"missing_per_column: {missing_per_column}")

#What are the variables of interest for your research questions?
def clean_spells(spells: pd.DataFrame) -> pd.DataFrame:
    clean_incantation = spells['Incantation'].notnull()
    spells = spells[clean_incantation]
    spells = spells.drop(columns= ['Name', 'Effect', 'Light'])
    #print(spells.columns)
    return spells

#Give a summary of each variable of interest.
def type_summary(spells: pd.DataFrame) -> dict[str, int]:
    counts = {}
    for types in spells['Type'].str.split(','):
        for type in types:
            type = type.strip()
            if type not in counts:
                counts[type] = 0
            counts[type]+= 1
    print(counts)
    return counts

#Create at least 2 visualizations
def bar_plot_type_counts(spells: pd.DataFrame) -> None:
    counts = type_summary(spells)
    counts_df = pd.DataFrame({'Type': list(counts.keys()),
                              'Count':list(counts.values())})
    sns.catplot(data = counts_df, x='Count', y='Type', kind='bar')
    plt.title('Types of Spells in Harry Potter')
    plt.xlabel('Counts')
    plt.ylabel('Types')
    plt.savefig('bar_plot_type_counts.png', bbox_inches='tight')

def pie_plot_type_counts(spells: pd.DataFrame) -> None:
    counts = type_summary(spells)
    attack_types = ['curse', 'hex', 'jinx', 'Transfiguration\xa0Jinx', 'Dark charm', 'Dark Arts']
    attack = 0
    non_attack = 0
    for spell_type, count in counts.items():
        if spell_type.lower() in attack_types:
            attack += count
        else:
            non_attack += count

    labels = ['Attack', 'Non-attack']
    sizes = [attack, non_attack]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels)
    ax.set_title("Attack Spells vs. Non-attack Spells")
    fig.savefig('pie_plot_type_counts.png', bbox_inches='tight')

###EDA for Characcters.csv
def load_characters (path: str) -> pd.DataFrame:
    characters = pd.read_csv(path, sep=';', na_values = ['Unknown'])
    return characters

#How large is your dataset?
def characters_size(characters: pd.DataFrame) -> None:
    """
    prints the number of rows and columns and the column names
    """
    rows, cols = characters.shape
    print(f"Rows: {rows}, Columns: {cols}")
    print(f"Columns: {list(characters.columns)}")

#Does your dataset have any missing data?
def find_missing(characters: pd.DataFrame) -> None:
    missing_per_column = characters.isnull().sum()
    print(f"missing_per_column: {missing_per_column}")

#Clean the data
def clean_characters(characters: pd.DataFrame) -> pd.DataFrame:
    characters = characters.drop(columns= ['Job',
                                           'Gender',
                                           'Wand',
                                           'Patronus',
                                           'Species',
                                           'Loyalty',
                                           'Hair colour',
                                           'Blood status',
                                           'Skills',
                                           'Eye colour',
                                           'Birth',
                                           'Death'])
    print(characters)
    return characters

def house_summary(characters: pd.DataFrame) -> None:
    print(characters['House'].value_counts())
    return characters['House'].value_counts()

def bar_plot_house_counts(characters: pd.DataFrame) -> None:
    counts = house_summary(characters)
    counts_df = pd.DataFrame({'House': counts.index,
                              'Count': counts.values})
    sns.catplot(data = counts_df, x='Count', y='House', kind='bar')
    plt.title('Number of Characters in Each House')
    plt.xlabel('Count')
    plt.ylabel('House')
    plt.savefig('bar_plot_house_counts.png', bbox_inches='tight')

def plot_shared_name(characters: pd.DataFrame) -> None:
    name = characters['Name'].str.split()
    last_name = name.str[-1]
    counts = last_name.value_counts()
    shared = counts[counts > 1]
    shared_df = pd.DataFrame({'Last name': shared.index,
                              'Count': shared.values})

    sns.catplot(data = shared_df, x='Count', y='Last name', kind='bar')
    plt.title('Last Names Shared More Than One Character')
    plt.xlabel('Number of Characters')
    plt.ylabel('Last name')
    plt.savefig('plot_shared_name.png', bbox_inches='tight')
    
###EDA for harry_potter_books.csv
def load_books(path: str) -> pd.DataFrame:
    books = pd.read_csv(path)
    return books

def books_size(books: pd.DataFrame) -> None:
    rows, cols = books.shape
    print(f"Rows: {rows}, Columns: {cols}")
    print(f"Columns: {list(books.columns)}")

def books_missing(books: pd.DataFrame) -> None:
    print("Missing Values")
    print(books.isnull().sum())

def combine_chapters(books: pd.DataFrame) -> pd.DataFrame:
    chapters = books.groupby(['book', 'chapter'], sort=False)['text'].apply(' '.join)
    chapters = chapters.reset_index()
    return chapters

def chapters_per_book(chapters: pd.DataFrame) -> pd.Series:
    return chapters['book'].value_counts()

def clean_book(chapters: pd.DataFrame) -> pd.DataFrame:
    text = chapters['text']
    text = text.str.replace('Mr.', 'Mr')
    text = text.str.replace('Mrs.', 'Mrs')
    text = text.str.replace('Dr.', 'Dr')
    chapters['text'] = text.str.strip()
    return chapters

def split_sentences(chapters: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i in range(len(chapters)):
        book = chapters['book'].iloc[i]
        chapter = chapters['chapter'].iloc[i]
        text = chapters['text'].iloc[i]
        parts = re.split(r'(?<=[.!?])\s+', text)
        for n in range(len(parts)):
            rows.append({'book': book, 'chapter': chapter, 'sentence_num': n, 'sentence': parts[n]})
        sentences = pd.DataFrame(rows)
        print(sentences)

        sentences = sentences['sentence'].str.lower()
        return sentences



def main():
    spells = load_spells('files/Spells.csv')
    spells_size(spells)
    find_missing_spells(spells)
    clean_spells(spells)
    type_summary(clean_spells(spells))
    bar_plot_type_counts(clean_spells(spells))
    pie_plot_type_counts(clean_spells(spells))

    characters = load_characters('files/Characters.csv')
    characters_size(characters)
    find_missing(characters)
    clean_characters(characters)
    house_summary(characters)
    bar_plot_house_counts(clean_characters(characters))
    plot_shared_name(clean_characters(characters))

    books = load_books('files/harry_potter_books.csv')
    books_size(books)
    books_missing(books)
    print(combine_chapters(books))
    chapters = combine_chapters(books)
    print(chapters_per_book(chapters))
    chapters = clean_book(chapters)
    sentences = split_sentences(chapters)
    






if __name__ == '__main__':
    main()
