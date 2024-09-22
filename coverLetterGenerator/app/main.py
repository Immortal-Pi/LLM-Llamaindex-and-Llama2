# stream lit for quick AI
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm,portfolio,clean_text):
    st.title('Cover Letter Generator')
    url_input = st.text_input('Enter URL:', value='https://jobs.nike.com/job/R-33460')
    submit_button = st.button('Submit')

    if submit_button:
        try:
            loader=WebBaseLoader([url_input])

            data=clean_text(loader.load().pop().page_content)

            portfolio.load_portfolio()

            jobs=llm.extract_jobs(data)
            # print(data)
            print(jobs)
            for job in jobs:
                skills=job.get('skills',[])

                links=portfolio.query_link(skills)

                cover_letter=llm.write_cover(job,links)
                # st.code(cover_letter,language='markdown')
                st.markdown(cover_letter)
        except Exception as e:
            st.error(f"An error occured: {e}")

if __name__=='__main__':
     chain=Chain()
     # print('chain')
     portfolio=Portfolio()
     # print('portfolio')
     st.set_page_config(layout='wide',page_title='Cover letter generator',page_icon='')
     create_streamlit_app(chain,portfolio,clean_text)