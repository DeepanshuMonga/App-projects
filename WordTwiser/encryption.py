import random
import streamlit as st
def coding_message(sentence):
    final_message_list=[]
    for word in sentence:
        c=0
        final_message=""
        temp_mesage=""
        for char in (word):
            c=c+1
        if(c>=3):
            l=len(word)
            for i,new_word in enumerate(word):
                if(i>=1):
                    temp_mesage=temp_mesage+new_word
                else: temp_mesage=""
            temp_mesage=temp_mesage+word[0]
            random_start=""
            random_end=""
            for i in range(0,3):
                random_integers=random.randint(97,122)
                random_char=(chr)(random_integers)
                random_start=random_start+random_char
            for i in range(0,3):
                random_integers=random.randint(97,122)
                random_char=(chr)(random_integers)
                random_end=random_end+random_char
            final_message=random_start+temp_mesage+random_end
            final_message_list.append(final_message)     
        else:
            leng=len(word)
            if(leng==2):
                final_message=word[1]+word[0]
            else:
                final_message=word
            final_message_list.append(final_message)
    return(final_message_list)
st.title("Welcome to WordTwister : ")
sentence=st.text_input("Enter your word/sentence :")
if(st.button("Submit")):
    word_list=(sentence.split(" "))
    final_list=coding_message(word_list)
    coded_message=""
    for word in final_list:
        coded_message=coded_message+word+" "
    st.subheader(f"Output is : {coded_message}")
